from django.views.generic import ListView
from django.contrib.auth import get_user_model 
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from ..models import AsuntosParticulares
from django.utils.decorators import method_decorator



@method_decorator(staff_member_required, name='dispatch')
class AsuntosParticularesListView(ListView):
    model = AsuntosParticulares
    template_name = 'admin/asuntosParticulares/listado_total_solicitudes.html'
    context_object_name = 'solicitudes'
    paginate_by = 20

    def get_queryset(self):
        """
        Sobrescribe el queryset para aplicar filtros dinámicamente.
        """
        queryset = super().get_queryset()
        
        # Obtiene los valores de los filtros desde la URL
        fecha_filtrada = self.request.GET.get('dia_solicitado')
        profesor_id = self.request.GET.get('profesor') # NUEVO: Obtener el ID del profesor

        # Aplica el filtro por fecha si se proporciona
        if fecha_filtrada:
            queryset = queryset.filter(dia_solicitado=fecha_filtrada)
        
        # Aplica el filtro por profesor si se proporciona
        if profesor_id: # NUEVO: Bloque para filtrar por profesor
            queryset = queryset.filter(profesor_id=profesor_id)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Añade los valores de los filtros y la lista de profesores al contexto.
        """
        context = super().get_context_data(**kwargs)
        context.update(**admin.site.each_context(self.request)) 
        context['title'] = 'Peticiones pendientes'
        
        # Pasa los valores actuales de los filtros para que los campos los recuerden
        context['dia_filtrado'] = self.request.GET.get('dia_solicitado', '')
        context['profesor_filtrado'] = self.request.GET.get('profesor', '') 
        User = get_user_model()
        # Pasa la lista de todos los usuarios para poblar el dropdown de profesores
        context['profesores'] = User.objects.all().order_by('email') 
        
        return context