from django.db import models
from ..models import Ausencia


class AusenciaComentario(models.Model):
    
    ausencia = models.ForeignKey(
            Ausencia,
            on_delete=models.CASCADE,
            related_name='comentarios',
            verbose_name="Ausencia"
        )

    comentario = models.TextField(
        max_length=500,
        verbose_name="Comentario"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    def __str__(self):
        return f"Comentario de {self.ausencia.profesor} - {self.fecha_creacion}"