from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator


class AsuntosParticulares(models.Model):
    """
    Modelo para gestionar las solicitudes de días de asuntos particulares.
    """
    # Choices para el campo relacion_juridica
    RELACION_CARRERA = 'carrera'
    RELACION_PRACTICAS = 'practicas'
    RELACION_INTERINO = 'interino'
    
    RELACION_JURIDICA_CHOICES = [
        (RELACION_CARRERA, 'Personal funcionario de carrera'),
        (RELACION_PRACTICAS, 'Personal funcionario en prácticas'),
        (RELACION_INTERINO, 'Personal funcionario interino'),
    ]
    
    # Choices para el campo jornada
    JORNADA_COMPLETA = 'completa'
    JORNADA_PARCIAL = 'parcial'

    JORNADA_CHOICES = [
        (JORNADA_COMPLETA, 'Completa'),
        (JORNADA_PARCIAL, 'Parcial'),
    ]
    
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_RECHAZADO = 'rechazado'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
    ]
    
    TURNO_DIURNO = 'diurno'
    TURNO_VESPERTINO = 'vespertino'
    
    TURNO_CHOICES = [
        (TURNO_DIURNO, 'Diurno'),
        (TURNO_VESPERTINO, 'Vespertino'),
    ]

    
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='asuntos_particulares',
        verbose_name="Profesor"
    )
    fecha_solicitud = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de Solicitud"
    )
    fecha_modificacion = models.DateField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    turno_solicitado = models.CharField(
        max_length=10,
        choices=TURNO_CHOICES,
        verbose_name="Turno Solicitado",
        default=TURNO_DIURNO
    )
    
    telefono = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^[67]\d{8}$',
                message="El número de teléfono debe tener 9 dígitos y empezar por 6 o 7."
            )
        ],
        verbose_name="Número de Teléfono"
    )
    
    relacion_juridica = models.CharField(
        max_length=10,
        choices=RELACION_JURIDICA_CHOICES,
        verbose_name="Relación Jurídica"
    )
    
    jornada = models.CharField(
        max_length=10,
        choices=JORNADA_CHOICES,
        verbose_name="Jornada"
    )
    
    hace_sustitucion = models.BooleanField(
        default=False,
        verbose_name="¿Estás haciendo una sustitución?"
    )
    
    retribuido = models.BooleanField(
        default=False,
        verbose_name="Estoy solicitando un día de permiso no retribuido"
    )
    
    dia_solicitado = models.DateField(
        verbose_name="Día Solicitado"
    )
    
    es_causa_sobrevenida = models.BooleanField(
        default=False,
        verbose_name="¿Causa sobrevenida?"
    )
    
    justificacion_causa_sobrevenida = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificación de la causa sobrevenida"
    )
    
    horas_afectadas = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name="Núm de horas de docencia directa y guardias afectadas"
    )
    
    dias_permiso_solicitados_centro = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(7)
        ],
        verbose_name="Núm de días de permisos solicitados en el centro"
    )
    
    consentimiento_grabacion = models.BooleanField(
        default=False,
        verbose_name="Entiendo que los datos del formulario, así como mi identidad, la fecha y hora de registro de la petición quedan grabadas automáticamente en el momento del envío del formulario."
    )
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        verbose_name="Estado de la Solicitud"
    )


    def __str__(self):
        # Es una buena práctica definir un método __str__
        return f"Solicitud de {self.profesor.get_full_name()}"

    class Meta:
        verbose_name = "Asunto Particular"
        verbose_name_plural = "Asuntos Particulares"