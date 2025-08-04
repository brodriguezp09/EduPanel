from django.db import models
import os
from ..models import CategoriaDocumento
from django.utils.text import slugify

def ruta_plantilla(instance, filename):
    """
    Genera una ruta de guardado dinámica para el archivo.
    Ejemplo: plantillas/permisos/nombre_del_archivo.docx
    """
    # Limpia el nombre de la categoría para usarlo como nombre de carpeta
    nombre_carpeta = instance.categoria.nombre.lower().replace(' ', '_')
    return os.path.join('plantillas', nombre_carpeta, filename)


class PlantillaDocumento(models.Model):
    """
    Modelo para gestionar plantillas documentales del centro educativo.
    """

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Plantilla",
        help_text="Ej: Solicitud de permiso por visita médica"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        editable=False,
        verbose_name="Slug (URL amigable)"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Breve explicación sobre el uso de la plantilla."
    )
    categoria = models.ForeignKey(
        CategoriaDocumento,
        on_delete=models.SET_NULL, # Si se borra una categoría, no se borran sus plantillas
        null=True,
        blank=True,
        verbose_name="Categoría"
    )
    archivo = models.FileField(
        upload_to=ruta_plantilla,
        verbose_name="Archivo de la Plantilla",
        help_text="Sube el documento (.docx, .pdf, .odt, etc.)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Genera el slug a partir del nombre antes de guardar
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Plantilla Documental"
        verbose_name_plural = "Plantillas Documentales"
        ordering = ['categoria', 'nombre']