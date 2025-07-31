from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from asuntosParticulares.models import AsuntosParticulares

@staff_member_required
def listar_solicitudes_pendientes_view(request):
    
    # 1. Obtenemos el valor del filtro de fecha desde la URL (parámetro GET)
    dia_filtrar = request.GET.get('dia_solicitado', None)
    
    # 2. Empezamos con el queryset base de solicitudes pendientes
    solicitudes_pendientes = AsuntosParticulares.objects.filter(
        estado=AsuntosParticulares.ESTADO_PENDIENTE
    )
    
    # 3. Si se proporcionó una fecha, aplicamos el filtro
    if dia_filtrar:
        # Este filtro se añade al anterior (estado='pendiente' Y dia_solicitado=...)
        solicitudes_pendientes = solicitudes_pendientes.filter(dia_solicitado=dia_filtrar)
    
    # Ordenamos el resultado final
    solicitudes_pendientes = solicitudes_pendientes.order_by('dia_solicitado')
    
    context = {
        **admin.site.each_context(request),
        'title': 'Peticiones pendientes',
        'solicitudes': solicitudes_pendientes,
        # 4. Pasamos el valor del filtro al contexto para mostrarlo en el input
        'dia_filtrado': dia_filtrar,
    }
    
    return render(request, 'admin/asuntosParticulares/gestionarPermisosListar.html', context)
