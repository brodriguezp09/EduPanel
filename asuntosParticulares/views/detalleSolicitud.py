from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from ..models import AsuntosParticulares
from ..utils.enviar_email import enviar_resolucion_email
from ..utils import generar_informe
from .enums import EstadoSolicitud
from datetime import datetime


@staff_member_required
def detalle_solicitud_view(request, pk):
    """
    Vista de detalle para una solicitud de Asuntos Particulares.
    Maneja tanto la visualización (GET) como las acciones (POST).
    """
    # OPTIMIZACIÓN 1: Usamos select_related para traer los datos del profesor
    # en la misma consulta a la base de datos, evitando un segundo hit.
    q = AsuntosParticulares.objects.select_related('profesor')
    solicitud_principal = get_object_or_404(q, pk=pk)
    
    primera_solicitud_profesor = AsuntosParticulares.objects.filter(
                profesor=solicitud_principal.profesor, 
                estado=AsuntosParticulares.ESTADO_APROBADO
            ).order_by('dia_solicitado').first()
        
    es_primera_solicitud = False
    if primera_solicitud_profesor is None or (primera_solicitud_profesor and primera_solicitud_profesor.pk == pk):
        es_primera_solicitud = True
    

    # --- Manejo de Acciones (Aprobar/Denegar) ---
    # OPTIMIZACIÓN 2: Se añade el manejo de peticiones POST para las acciones.
    if request.method == 'POST' and 'action' in request.POST:
        #obtenemos la solicitudes ordenadas por fecha para saber si es la primera
        
        datos_informe = {
                "{{Nombre}}": solicitud_principal.profesor.first_name,
                "{{Apellidos}}": solicitud_principal.profesor.last_name,
                "{{dia}}": solicitud_principal.dia_solicitado.strftime("%d"),
                "{{mes}}": solicitud_principal.dia_solicitado.strftime("%B"),
                "{{anio}}": solicitud_principal.dia_solicitado.strftime("%Y"),
                "{{resolucion}}": "Acepto",
                "{{diaRel}}": datetime.now().strftime("%d"),
                "{{mesRel}}": datetime.now().strftime("%B"),
                "{{anioRel}}": datetime.now().strftime("%Y"),
                "{{selloTiempo}}": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
            
        if request.POST['action'] == 'approve':
            
            solicitud_principal.estado = AsuntosParticulares.ESTADO_APROBADO
            solicitud_principal.save()
            solicitud_principal.profesor.dias_asuntos_propios_disfrutados = solicitud_principal.profesor.dias_asuntos_propios_disfrutados + 1
            solicitud_principal.profesor.save()
            
            datos_informe['{{resolucion}}'] = "Acepto"
            
            informe = generar_informe(datos_informe)
            
            enviar_resolucion_email(
                resolucion=EstadoSolicitud.CONCEDER_PRIMER if es_primera_solicitud else EstadoSolicitud.CONCEDER,
                user_email=solicitud_principal.profesor.email,
                buffer_documento=informe
            )
            
            messages.success(request, "La solicitud ha sido APROBADA.")
            
        elif request.POST['action'] == 'deny':
            solicitud_principal.estado = AsuntosParticulares.ESTADO_RECHAZADO
            solicitud_principal.save()
            if solicitud_principal.profesor.dias_asuntos_propios_disfrutados > 0:
                solicitud_principal.profesor.dias_asuntos_propios_disfrutados = solicitud_principal.profesor.dias_asuntos_propios_disfrutados -1
                solicitud_principal.profesor.save()
                
            resul = EstadoSolicitud.DENEGAR
            if diferencia_mayor_a_15_dias(str(solicitud_principal.dia_solicitado), str(solicitud_principal.fecha_solicitud)) == False and solicitud_principal.es_causa_sobrevenida==False:
                resul = EstadoSolicitud.DENEGAR_15
            
            datos_informe['{{resolucion}}'] = "Rechazo"
            
            informe = generar_informe(datos_informe)
                
            enviar_resolucion_email(
                resolucion=resul,
                user_email=solicitud_principal.profesor.email,
                buffer_documento=informe)
            
            messages.error(request, "La solicitud ha sido DENEGADA.")
        
        # Redirigimos a la misma página para evitar reenvío del formulario.
        return redirect(reverse('admin:detalle_solicitud', args=[pk]))

    # --- Preparación de Datos para la Plantilla (GET) ---

    # OPTIMIZACIÓN 3: Hacemos esta consulta UNA SOLA VEZ y la reutilizamos.
    solicitudes_profesor = AsuntosParticulares.objects.filter(
        profesor=solicitud_principal.profesor
    )

    # La agregación es eficiente, la mantenemos.
    conteo_por_estado = solicitudes_profesor.values('estado').annotate(
        total=Count('estado')
    ).order_by('estado')

    # Obtenemos otras solicitudes del mismo día.
    otras_solicitudes_mismo_dia = AsuntosParticulares.objects.filter(
        dia_solicitado=solicitud_principal.dia_solicitado
    ).exclude(pk=pk)
    
    context = {
        **admin.site.each_context(request),
        'title': f"Solicitud: {solicitud_principal.profesor.get_full_name()}",
        'solicitud': solicitud_principal,
        'conteo_estados': conteo_por_estado,
        'dias_totales_disponibles': solicitud_principal.profesor.dias_asuntos_propios,
        'otras_solicitudes': otras_solicitudes_mismo_dia,
        'es_primera_solicitud': es_primera_solicitud, # Usamos una variable clara.
    }
    
    return render(request, 'admin/asuntosParticulares/detalle_solicitud.html', context)


def diferencia_mayor_a_15_dias(fecha1_str, fecha2_str):
    '''
    Comprueba si la diferencia entre dos fechas es mayor a 15 días.
    Asume que fecha1_str es una fecha en formato "YYYY-MM-D" y fecha2_str es una fecha en formato "YYYY-MM-DD HH:MM:SS+00:00".
    '''
    # Parsear fecha1: formato "YYYY-MM-D"
    fecha1 = datetime.strptime(fecha1_str, "%Y-%m-%d")

    # Parsear fecha2: formato "YYYY-MM-DD HH:MM:SS+00:00"
    # Usamos fromisoformat que soporta fechas ISO con zona horaria
    fecha2 = datetime.fromisoformat(fecha2_str)

    # Restamos fechas (ignoramos la parte de hora/zona)
    diferencia = abs((fecha2.date() - fecha1.date()).days)
    return diferencia > 15