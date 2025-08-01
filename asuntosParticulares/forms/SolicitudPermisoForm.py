from django import forms
from asuntosParticulares.models import AsuntosParticulares, validar_solo_pdf

class SolicitudPermisoForm(forms.ModelForm):
    # Campos ocultos para pasar datos desde el calendario (Alpine.js) al backend
    dia_solicitado = forms.DateField(widget=forms.HiddenInput())
    turno_solicitado = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = AsuntosParticulares
        # Incluimos todos los campos que el usuario debe rellenar
        fields = [
            'dia_solicitado', 
            'turno_solicitado',
            'telefono', 
            'relacion_juridica', 
            'jornada', 
            'hace_sustitucion', 
            'retribuido', 
            'es_causa_sobrevenida', 
            'justificacion_causa_sobrevenida', 
            'horas_afectadas', 
            'dias_permiso_solicitados_centro', 
            'consentimiento_grabacion',
            'archivo_adjunto'
        ]
        widgets = {
            'justificacion_causa_sobrevenida': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el campo de consentimiento sea obligatorio
        self.fields['consentimiento_grabacion'].required = True
        self.fields['archivo_adjunto'].validators.append(validar_solo_pdf)

        # --- Personalización de estilos ---
        # Usamos Tailwind CSS para los estilos de los campos del formulario

        # Aplicamos clases de Tailwind a todos los campos
        tailwind_classes = "block w-full rounded-md border-0 py-1.5 text-gray-900 bg-gray-50 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary-500 sm:text-sm sm:leading-6"
        checkbox_classes = "focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"

        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                 field.widget.attrs.update({'class': checkbox_classes})
            elif field.widget.__class__.__name__ != 'HiddenInput':
                field.widget.attrs.update({'class': tailwind_classes})
        

