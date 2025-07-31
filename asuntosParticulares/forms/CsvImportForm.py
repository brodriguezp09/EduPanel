from django import forms

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Fichero CSV",
        widget=forms.FileInput(attrs={'class': 'custom-file-input'})
    )