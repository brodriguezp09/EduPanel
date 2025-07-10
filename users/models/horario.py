
from django.db import models
from .user import CustomUser

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Asignatura")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"


class Horario(models.Model):
    """
    Modelo para cada franja horaria de un profesor.
    Conecta un usuario, una asignatura, un día y una hora.
    """
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]

    HORAS_CLASE = [
        ('1ª', '08:30 - 09:25'),
        ('2ª', '09:25 - 10:20'),
        ('3ª', '10:20 - 11:15'),
        ('4ª', '11:45 - 12:40'),
        ('5ª', '12:40 - 13:35'),
        ('6ª', '13:35 - 14:30'),
        ('7ª', '16:00 - 16:55'),
        ('8ª', '16:55 - 17:50'),
        ('9ª', '17:50 - 18:45'),
        ('10ª', '19:00 - 19:55'),
        ('11ª', '19:55 - 20:50'),
        ('12ª', '20:50 - 21:45'),
    ]

    profesor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='horarios',
        verbose_name="Profesor"
    )
    asignatura = models.ForeignKey(
        Asignatura, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Asignatura"
    )
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA, verbose_name="Día")
    hora = models.CharField(max_length=5, choices=HORAS_CLASE, verbose_name="Hora")

    class Meta:
        verbose_name = "Franja Horaria"
        verbose_name_plural = "Franjas Horarias"
        # Nos aseguramos de que un profesor no pueda tener dos clases a la misma hora el mismo día
        unique_together = ('profesor', 'dia', 'hora')

    def __str__(self):
        return f"{self.profesor.username} - {self.dia} a las {self.get_hora_display()} - {self.asignatura.nombre}"
