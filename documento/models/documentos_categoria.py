from django.db import models
from colorfield.fields import ColorField

class CategoriaDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    color = ColorField(default='#FFFFFF', verbose_name="Color de la Categoría")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría de Documento"
        verbose_name_plural = "Categorías de Documentos"
        ordering = ['nombre']
