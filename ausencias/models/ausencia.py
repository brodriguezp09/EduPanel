from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Ausencia(models.Model):
    """
    Modelo para gestionar las ausencias de los profesores.
    """
    
    ESTADO_AUSENCIA = [
        ('pendiente', 'Pendiente de Justificación'),
        ('justificada_profesor', 'Justificada Profesor'),
        ('pendiente_subsanacion', 'Pendiente de Subsanación'),
        ('justificada', 'Justificada'),
        ('tramitada', 'Tramitada')
    ]
    
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ausencias',
        verbose_name="Usuario"
    )
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_AUSENCIA,
        default='pendiente',
        verbose_name="ausencia"
    )
    fecha_dia_justificado_inicio = models.DateField(
        help_text="Primer día del periodo justificado."
    )
    fecha_dia_justificado_fin = models.DateField(
        help_text="Último día del periodo justificado."
    )
    
    def clean(self):
        # Primero, nos aseguramos de que ambas fechas existen antes de comparar
        if self.fecha_dia_justificado_inicio and self.fecha_dia_justificado_fin:
            # 1. Comprobamos que la fecha de fin no sea anterior a la de inicio
            if self.fecha_dia_justificado_fin < self.fecha_dia_justificado_inicio:
                raise ValidationError({
                    'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
                })

            # 2. Calcular la duración del rango
            duracion = self.fecha_dia_justificado_fin - self.fecha_dia_justificado_inicio

            # 3. Validamos que la duración no sea superior a 6 días
            # Sumamos 1 a los días porque un rango de 'hoy' a 'hoy' es 1 día de duración (0 días de diferencia)
            if duracion.days + 1 > 6:
                raise ValidationError(
                    'El rango de fechas no puede ser superior a 6 días. '
                    f'Actualmente es de {duracion.days + 1} días.'
                )
    