from django.contrib import admin
from .models import PlantillaDocumento, CategoriaDocumento

@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color')
    search_fields = ('nombre',)

@admin.register(PlantillaDocumento)
class PlantillaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'categoria', 'fecha_actualizacion')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion')
    autocomplete_fields = ['categoria']
    readonly_fields = ('slug',)

