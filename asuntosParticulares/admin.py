from django.contrib import admin
from .models import AsuntosParticulares, DiaFestivo
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .forms import CsvImportForm
from .views import listar_solicitudes_pendientes_view, detalle_solicitud_view, AsuntosParticularesListView
import csv
import io
from datetime import datetime

@admin.register(AsuntosParticulares)
class AsuntosParticularesAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo AsuntosParticulares.
    """
    list_display = ('profesor', 'estado','dia_solicitado', 'fecha_solicitud', 'turno_solicitado')
    list_filter = ('profesor', 'jornada', 'retribuido', 'es_causa_sobrevenida', 'dia_solicitado')
    search_fields = ('profesor__first_name', 'profesor__last_name', 'profesor__username', 'justificacion_causa_sobrevenida')
    date_hierarchy = 'dia_solicitado'
    readonly_fields = ('fecha_solicitud', 'fecha_modificacion')
    fieldsets = (
        ('Información del Solicitante', {
            'fields': ('profesor', 'telefono')
        }),
        ('Detalles de la Solicitud', {
            'fields': ('estado','dia_solicitado', 'turno_solicitado','jornada', 'relacion_juridica', 'hace_sustitucion', 'retribuido', 'horas_afectadas')
        }),
        ('Causa Sobrevenida', {
            'fields': ('es_causa_sobrevenida', 'justificacion_causa_sobrevenida')
        }),
        ('Información Adicional', {
            'fields': ('dias_permiso_solicitados_centro', 'consentimiento_grabacion')
        }),
        ('Fechas de Registro', {
            'fields': ('fecha_solicitud', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('informe/', self.admin_site.admin_view(listar_solicitudes_pendientes_view), name='informe_permisos'),
            path('informes/', self.admin_site.admin_view(AsuntosParticularesListView.as_view()), name='informe_permisos_totales'),
            path('<int:pk>/detalle/', self.admin_site.admin_view(detalle_solicitud_view), name='detalle_solicitud'),
        ]
        return custom_urls + urls

@admin.register(DiaFestivo)
class DiaFestivoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo DiaFestivo.
    """
    list_display = ('fecha', 'motivo')
    search_fields = ('motivo',)
    ordering = ('fecha',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-festivos-csv/', self.import_csv, name='asuntosParticulares_diafestivo_import'),

        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'El fichero no es un CSV.')
                    return redirect("..")

                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.reader(io_string, delimiter=';')
                    next(reader)  # Saltar la cabecera

                    festivos_creados = 0
                    for row in reader:
                        if not row: continue # Omitir filas vacías
                        
                        fecha_str, motivo = row
                        
                        # Convertir la fecha de formato dd/mm/YYYY a YYYY-MM-DD
                        fecha_obj = datetime.strptime(fecha_str.strip(), '%d/%m/%Y').date()

                        # Crear o actualizar el día festivo para evitar duplicados
                        dia_festivo, created = DiaFestivo.objects.update_or_create(
                            fecha=fecha_obj,
                            defaults={'motivo': motivo.strip()}
                        )
                        if created:
                            festivos_creados += 1
                    
                    messages.success(request, f"Se han importado y creado {festivos_creados} nuevos días festivos.")
                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al procesar el fichero: {e}")
                
                return redirect("..")
        
        form = CsvImportForm()
        payload = {"form": form, "title": "Importar Días Festivos desde CSV"}
        #context = self.admin_site.each_context(request)
        
        payload.update(self.admin_site.each_context(request))
        return render(request, "admin/csv_form.html", payload)  
