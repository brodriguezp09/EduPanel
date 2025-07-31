from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
import json

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
    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Solicitud"
    )
    fecha_modificacion = models.DateTimeField(
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
        
    def to_json(self):
        """
        Serializa los datos de la solicitud a un string JSON seguro para usar en JavaScript.
        """
        if self.estado == self.ESTADO_APROBADO:
            estado_html = '<span class="inline-flex items-center rounded-md bg-green-500/10 px-2 py-1 text-xs font-medium text-green-400 ring-1 ring-inset ring-green-500/20">Aprobado</span>'
        elif self.estado == self.ESTADO_PENDIENTE:
            estado_html = '<span class="inline-flex items-center rounded-md bg-yellow-400/10 px-2 py-1 text-xs font-medium text-yellow-500 ring-1 ring-inset ring-yellow-400/20">Pendiente</span>'
        else:
            estado_html = '<span class="inline-flex items-center rounded-md bg-red-400/10 px-2 py-1 text-xs font-medium text-red-400 ring-1 ring-inset ring-red-400/30">Rechazado / Cancelado</span>'

        return json.dumps({
            'pk': self.pk,
            'dia_solicitado': self.dia_solicitado.strftime('%d/%m/%Y'),
            'turno': self.get_turno_solicitado_display(),
            'estado': self.estado,
            'estado_html': estado_html,
            'fecha_solicitud': self.fecha_solicitud.strftime('%d/%m/%Y'),
            'fecha_modificacion': self.fecha_modificacion.strftime('%d/%m/%Y'),
            'telefono': self.telefono,
            'relacion_juridica': self.get_relacion_juridica_display(),
            'jornada': self.get_jornada_display(),
            'hace_sustitucion': "Sí" if self.hace_sustitucion else "No",
            'retribuido': "Sí" if self.retribuido else "No",
            'es_causa_sobrevenida': "Sí" if self.es_causa_sobrevenida else "No",
            'justificacion_causa': self.justificacion_causa_sobrevenida or "No se ha proporcionado justificación.",
            'horas_afectadas': self.horas_afectadas,
            'dias_permiso_solicitados_centro': self.dias_permiso_solicitados_centro,
        })

