from django.db import models

class DiaFestivo(models.Model):
    """
    Modelo para almacenar los días festivos del calendario escolar.
    """
    fecha = models.DateField(
        unique=True,
        verbose_name="Fecha"
    )
    motivo = models.CharField(
        max_length=255,
        verbose_name="Motivo del festivo"
    )

    def __str__(self):
        # Formatea la fecha al formato dd/mm/YYYY para una mejor visualización
        return f"{self.fecha.strftime('%d/%m/%Y')} - {self.motivo}"

    class Meta:
        verbose_name = "Día Festivo"
        verbose_name_plural = "Días Festivos"
        ordering = ['fecha']