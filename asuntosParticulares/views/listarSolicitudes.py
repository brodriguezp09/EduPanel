from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from asuntosParticulares.models import AsuntosParticulares


class MisSolicitudesView(LoginRequiredMixin, ListView):
    model = AsuntosParticulares
    template_name = 'asuntos/mis_solicitudes.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        """
        Esta función se asegura de que cada usuario solo vea sus propias solicitudes,
        ordenadas de la más reciente a la más antigua.
        """
        return AsuntosParticulares.objects.filter(profesor=self.request.user).order_by('-fecha_solicitud')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = {
        'dias_ya_solicitados': self.request.user.dias_asuntos_propios_disfrutados,
        'dias_totales_disponibles': self.request.user.dias_asuntos_propios,
        'dias_restantes': self.request.user.dias_asuntos_propios - self.request.user.dias_asuntos_propios_disfrutados,
        'solicitudes': self.get_queryset(),
    }
        return context


