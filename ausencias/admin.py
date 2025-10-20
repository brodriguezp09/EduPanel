from django.contrib import admin
from .models import Ausencia

# Register your models here.
@admin.register(Ausencia)
class AusenciaAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'estado','fecha_dia_justificado_inicio', 'fecha_dia_justificado_fin')
    list_filter = ('profesor', 'fecha_dia_justificado_inicio')
    search_fields = ('profesor__first_name', 'profesor__last_name', 'profesor__username', 'fecha_dia_justificado_inicio')