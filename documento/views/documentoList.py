from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import PlantillaDocumento

class DocumentoListView(LoginRequiredMixin, ListView):
    model = PlantillaDocumento
    template_name = 'documento/documento_list.html'
    context_object_name = 'documentos'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Filtra los resultados si se proporciona un parámetro de búsqueda 'q'.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            # Filtra por el campo 'nombre' si hay un término de búsqueda
            queryset = queryset.filter(nombre__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Pasa el término de búsqueda de vuelta a la plantilla.
        """
        context = super().get_context_data(**kwargs)
        # Esto permite que el campo de búsqueda "recuerde" lo que se buscó
        context['search_query'] = self.request.GET.get('q', '')
        return context