from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Clases de Tailwind para los campos
        tailwind_classes = "block w-full rounded-md border-0 py-1.5 text-gray-900 bg-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-primary-500 sm:text-sm sm:leading-6"

        # Aplicar estilos a cada campo del formulario
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': tailwind_classes})
            field.help_text = '' # Opcional: elimina los textos de ayuda por defecto
