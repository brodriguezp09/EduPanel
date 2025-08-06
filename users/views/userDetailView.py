from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import CustomUser, Horario

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/user_detail.html'
    context_object_name = 'profesor'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profesor = self.get_object()

        # Obtenemos el horario del profesor y lo ordenamos
        dias_orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        horarios = Horario.objects.filter(profesor=profesor)
        
        # Estructuramos el horario para la plantilla
        horario_estructurado = {dia: [] for dia in dias_orden}
        for h in horarios:
            horario_estructurado[h.dia].append(h)
        
        context['horario_semanal'] = horario_estructurado
        
        context['title'] = f"Detalle de {profesor.get_full_name()}"
        return context