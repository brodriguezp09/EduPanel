from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from asuntosParticulares.models import AsuntosParticulares
from django.shortcuts import render

@login_required
def cancelar_solicitud_confirm_view(request, pk):
    """
    Muestra la página de confirmación antes de cancelar una solicitud.
    """
    solicitud = get_object_or_404(AsuntosParticulares, pk=pk, profesor=request.user)
    
    # Si la solicitud no está pendiente, no se puede cancelar
    if solicitud.estado != AsuntosParticulares.ESTADO_PENDIENTE:
        messages.error(request, 'Esta solicitud ya no se puede cancelar.')
        return redirect('asuntosParticulares:mis_solicitudes')
        
    return render(request, 'asuntos/cancelar_solicitud_confirm.html', {'solicitud': solicitud})


@login_required
def cancelar_solicitud_view(request, pk):
    """
    Procesa la cancelación de una solicitud (solo acepta POST).
    """
    if request.method == 'POST':
        solicitud = get_object_or_404(AsuntosParticulares, pk=pk, profesor=request.user)

        if solicitud.estado == AsuntosParticulares.ESTADO_PENDIENTE:            
            solicitud.delete()
            messages.success(request, 'La solicitud ha sido cancelada correctamente.')
        else:
            messages.error(request, 'No se puede cancelar una solicitud que ya ha sido procesada.')
    
    return redirect('asuntosParticulares:mis_solicitudes')
