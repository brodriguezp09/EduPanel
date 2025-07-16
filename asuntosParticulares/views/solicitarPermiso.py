from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import calendar
from asuntosParticulares.models import DiaFestivo, AsuntosParticulares
from django.db.models import Count
from asuntosParticulares.forms import SolicitudPermisoForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import F
from users.models import CustomUser 

@login_required
def solicitar_permiso_view(request):
    # --- Lógica para procesar el formulario (POST con AJAX) ---
    if request.method == 'POST':
        # ... (La lógica del POST se mantiene igual)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = SolicitudPermisoForm(request.POST)
            if form.is_valid():
                solicitud = form.save(commit=False)
                solicitud.profesor = request.user
                solicitud.save()
                #actualizamos el número de días de asuntos propios disfrutados
                CustomUser.objects.filter(pk=request.user.pk).update(
                    dias_asuntos_propios_disfrutados=F('dias_asuntos_propios_disfrutados') + 1
        )
                return JsonResponse({'success': True, 'message': '¡Solicitud enviada correctamente!'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        return redirect('asuntosParticulares:solicitar_permiso')

    # --- Lógica para mostrar la página (GET) ---
    dias_ya_solicitados = AsuntosParticulares.objects.filter(
        profesor=request.user,
        estado__in=[AsuntosParticulares.ESTADO_APROBADO, AsuntosParticulares.ESTADO_PENDIENTE]
    ).count()
    
    # Obtenemos los días totales y comprobamos si el usuario puede solicitar más
    dias_totales_disponibles = request.user.dias_asuntos_propios
    dias_restantes = dias_totales_disponibles - dias_ya_solicitados
    puede_solicitar = dias_ya_solicitados < dias_totales_disponibles
    
    print(f"puede_solicitar: {puede_solicitar}, dias_ya_solicitados: {dias_ya_solicitados}, dias_totales_disponibles: {dias_totales_disponibles}, dias_restantes: {dias_restantes}")
    
    
    form = SolicitudPermisoForm(initial={'dias_permiso_solicitados_centro': dias_ya_solicitados})

    # --- Lógica para generar el calendario ---
    MAX_DIURNO = 4
    MAX_VESPERTINO = 2
    festivos = {f.fecha: f.motivo for f in DiaFestivo.objects.all()}
    today = date.today()
    
    # --- CORRECCIÓN ---
    # Ahora la búsqueda de días laborables empieza desde HOY, no desde mañana.
    dias_laborables = []
    dia_actual = today 
    dias_revisados = 0 # Bucle de seguridad
    while len(dias_laborables) < 90 and dias_revisados < 180:
        if dia_actual.weekday() < 5 and dia_actual not in festivos:
            dias_laborables.append(dia_actual)
        dia_actual += timedelta(days=1)
        dias_revisados += 1
    # --- FIN DE LA CORRECCIÓN ---

    if not dias_laborables:
        context = {
            'calendario_meses': [], 
            'form': form,
            'puede_solicitar': puede_solicitar,
            'dias_ya_solicitados': dias_ya_solicitados,
            'dias_totales_disponibles': dias_totales_disponibles,
            'dias_restantes': dias_restantes,
        }
        return render(request, 'asuntos/solicitar_permiso.html', context)

    # El resto de la lógica ahora funcionará correctamente porque el rango de fechas incluye hoy
    primer_dia_calendario = dias_laborables[0]
    ultimo_dia_calendario = dias_laborables[-1]

    solicitudes_contadas = AsuntosParticulares.objects.filter(
        dia_solicitado__range=[primer_dia_calendario, ultimo_dia_calendario],
        estado__in=[AsuntosParticulares.ESTADO_APROBADO, AsuntosParticulares.ESTADO_PENDIENTE]
    ).values('dia_solicitado', 'turno_solicitado').annotate(total=Count('id'))

    cupos_usados = {}
    for solicitud in solicitudes_contadas:
        dia = solicitud['dia_solicitado']
        if dia not in cupos_usados:
            cupos_usados[dia] = {'diurno': 0, 'vespertino': 0}
        cupos_usados[dia][solicitud['turno_solicitado']] = solicitud['total']

    calendario_final = []
    mes_actual = date(primer_dia_calendario.year, primer_dia_calendario.month, 1)
    
    while mes_actual <= ultimo_dia_calendario:
        month_calendar = calendar.monthcalendar(mes_actual.year, mes_actual.month)
        semanas_del_mes = []
        for week in month_calendar:
            semana_procesada = []
            for day_num in week:
                day_info = {"dia": day_num, "es_laborable": False, "es_festivo": False}
                if day_num != 0:
                    current_day_date = date(mes_actual.year, mes_actual.month, day_num)
                    day_info["fecha"] = current_day_date
                    day_info["weekday"] = current_day_date.weekday()
                    if current_day_date in festivos:
                        day_info["es_festivo"] = True
                        day_info["motivo_festivo"] = festivos[current_day_date]
                    elif current_day_date.weekday() < 5 and current_day_date >= today:
                        day_info["es_laborable"] = True
                        usados_diurno = cupos_usados.get(current_day_date, {}).get('diurno', 0)
                        usados_vespertino = cupos_usados.get(current_day_date, {}).get('vespertino', 0)
                        day_info['disponibles_diurno'] = MAX_DIURNO - usados_diurno
                        day_info['disponibles_vespertino'] = MAX_VESPERTINO - usados_vespertino
                semana_procesada.append(day_info)
            semanas_del_mes.append(semana_procesada)
        
        calendario_final.append({
            'fecha_mes': mes_actual,
            'semanas': semanas_del_mes,
        })
        
        next_month = mes_actual.month + 1
        next_year = mes_actual.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        mes_actual = date(next_year, next_month, 1)
        
    context = {
        'calendario_meses': calendario_final, 
        'form': form,
        'puede_solicitar': puede_solicitar,
        'dias_ya_solicitados': dias_ya_solicitados,
        'dias_totales_disponibles': dias_totales_disponibles,
        'dias_restantes': dias_restantes,
    }
    return render(request, 'asuntos/solicitar_permiso.html', context)
