from django import forms

class CsvImportForm(forms.Form):
    """
    Un formulario simple para gestionar la subida de ficheros CSV.
    """
    csv_file = forms.FileField(label="Seleccionar fichero CSV")