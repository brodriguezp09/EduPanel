from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ..models import Ausencia

class AnexoV(models.Model):
    """
    Modelo para almacenar la información del Anexo V de un profesor.
    """
    # --- Choices para los campos de tipo select ---
    
    CUERPO_CHOICES = [
        ('secundaria', 'Profesor enseñanza Secundaria'),
        ('formacion_profesional', 'Profesor Formación Profesional'),
    ]

    GRUPO_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]

    RELACION_JURIDICA_CHOICES = [
        ('carrera', 'Personal funcionario de carrera'),
        ('indefinido', 'Personal laboral indefinido'),
        ('practicas', 'Personal funcionario en prácticas'),
        ('temporal', 'Personal laboral temporal'),
        ('interino', 'Personal funcionario interino'),
    ]
    
    JORNADA_CHOICES = [
        ('completa', 'Jornada Completa'),
        ('parcial', 'Jornada Parcial'),
    ]

    PERMISO_SOLICITUD_CHOICES = [
        ('fallecimiento', 'Por fallecimiento, accidente o enfermedad grave, hospitalización o intervención quirúrgica de un familiar (art. 2).'),
        ('enfermedad', 'Por enfermedad propia (art. 3).'),
        ('traslado','Por traslado de domicilio (art. 4).'),
        ('examen', 'Realización de exámenes prenatales y técnicas de preparación al parto (art. 7).'),
        ('reproduccion', 'Para técnicas de fecundación o reproducción asistida (art. 8).'),
        ('interrupcion', 'Por interrupción voluntaria del embarazo (art. 9).'),
        ('deber inexcusable', 'Para el cumplimiento de un deber inexcusable de carácter público o personal y por deberes relacionados con la conciliación de la vida familiar y laboral (art. 11).'),
        ('asuntos particulares', 'Por asuntos particulares (art. 12).'),
        ('sindicato','Para realización de funciones sindicales de formación sindical o de representación del personal (art. 13).'),
        ('prueba pública', 'Para concurrir a exámenes finales, pruebas obligatorias deaptitud, evaluación en centros oficiales y pruebas selectivas en el ámbito del empleo público (art. 14).'),
        ('violencia de género', 'Por razón de violencia de género (art. 20).'),
        ('reducción jornada', 'Por reducción de jornada (art. 30).'),

    ]
    
    DOCUMENTACION_CHOICES = [
    ('LFD', 'Fotocopia cotejada del libro de familia/DNI.'),
    ('EMP', 'Certificado de empadronamiento.'),
    ('DEF', 'Certificado de defunción.'),
    ('PAH', 'Fotocopia cotejada de la inscripción en el Registro Oficial de Parejas de Hecho.'),
    ('HOS', 'Documento que acredite la hospitalización o la intervención quirúrgica grave según el motivo que genera la solicitud del permiso.'),
    ('NAD', 'Fotocopia cotejada de la partida de nacimiento o de la resolución administrativa o judicial de adopción o acogimiento.'),
    ('CON', 'Certificado de convivencia o informe del trabajador social en el que acredite a las personas que conforman la unidad familiar.'),
    ('EXO', 'Documento acreditativo de la asistencia a la prueba de aptitud, examen final o prueba de acceso o ingreso a la función pública en el que figure el lugar, la fecha y el centro de realización de los mismos.'),
    ('EPR', 'Documento justificativo de la necesidad de realización de exámenes prenatales y técnicas de preparación al parto dentro de la jornada laboral.'),
    ('SAD', 'Documento justificativo de la necesidad de asistencia a las preceptivas sesiones de información y preparación y para la realización de los preceptivos informes psicológicos y sociales previos a la declaración de idoneidad dentro de la jornada laboral.'),
    ('TFE', 'Documento justificativo de la necesidad de realización de tratamientos de fecundación asistida dentro de la jornada laboral.'),
    ('RME', 'Documento justificativo de la necesidad de realización de las revisiones médicas dentro de la jornada laboral.'),
    ('AME', 'Documento acreditativo de las limitaciones que les impiden ir solos o de que no pueden valerse por sí mismo (acompañamiento a las revisiones médicas).'),
    ('COF', 'Original o copia cotejada de la citación o convocatoria del órgano judicial, administrativo, órgano de gobierno o comisión dependiente de los mismos o cualquier otro órgano oficial.'),
    ('MEL', 'Documento acreditativo de tener la condición de elegible en el proceso electoral o de formar parte de una mesa electoral.'),
    ('ROF', 'Original o copia cotejada de la convocatoria o/y asistencia a reunión de las comisiones de las pruebas de acceso a la universidad, de la Consejería de Educación o de las Delegaciones Provinciales o del órgano de selección o provisión, con nombramiento de la autoridad competente.'),
    ('OLE', 'Documento que acredite la responsabilidad civil, penal, social o administrativa del interesado y que suponga el cumplimiento de una obligación.'),
    ('DSA', 'Documento que acredite la donación de sangre, médula o plaquetas.'),
    ('DAN', 'Documento que acredite la asistencia de los deportistas de alto nivel a las competiciones de carácter internacional, así como las concentraciones preparatorias de estas.'),
    ('OTR', 'Otros'),
]

    # --- Campos del modelo ---
    ausencia = models.ForeignKey(
        Ausencia,
        on_delete=models.CASCADE,
        related_name='anexos',
        verbose_name="Ausencia"
    )

    dni = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}[A-Z]$',
                message="El DNI debe tener 8 números y una letra mayúscula."
            )
        ],
        verbose_name="DNI"
    )

    telefono = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^[679]\d{8}$',
                message="El número de teléfono debe tener 9 dígitos y empezar por 6, 7 o 9."
            )
        ],
        verbose_name="Teléfono"
    )

    cuerpo = models.CharField(
        max_length=30,
        choices=CUERPO_CHOICES,
        default='secundaria',
        verbose_name="Cuerpo"
    )

    grupo = models.CharField(
        max_length=2,
        choices=GRUPO_CHOICES,
        default='A1',
        verbose_name="Grupo"
    )

    subgrupo = models.PositiveIntegerField(
        default=24,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(30)
        ],
        verbose_name="Subgrupo"
    )

    relacion_juridica = models.CharField(
        max_length=20,
        choices=RELACION_JURIDICA_CHOICES,
        verbose_name="Relación Jurídica"
    )
    
    jornada = models.CharField(
        max_length=20,
        choices=JORNADA_CHOICES,
        default='completa',
        verbose_name="Jornada"
    )
    
    permiso_solicitado = models.CharField(
        max_length=50,
        choices=PERMISO_SOLICITUD_CHOICES,
        verbose_name="Permiso Solicitado"
    )
    
    documentacion_aportada = models.CharField(
        max_length=150,
        choices=DOCUMENTACION_CHOICES,
        verbose_name="Documentación Aportada"
    )

    fecha_realizacion_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Solicitud"
    )
    
    fecha_modificacion_solicitud = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    fecha_dia_justificado_inicio = models.DateField(
        help_text="Primer día del periodo justificado."
    )
    fecha_dia_justificado_fin = models.DateField(
        help_text="Último día del periodo justificado."
    )
    
    hora_inicio = models.TimeField(
        help_text="Hora de inicio del periodo justificado."
    )
    hora_final = models.TimeField(
        help_text="Hora de finalización del periodo justificado."
    )
    
    horas_lectivas_afectadas = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name="Horas Lectivas Afectadas"
    )
    
    horas_no_lectivas_afectadas = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        verbose_name="Horas Lectivas Afectadas"
    )
    
    
    
    
    def __str__(self):
        return f"Anexo V de {self.usuario.get_full_name() or self.usuario.username}"
    
    def clean(self):
                
        # validacion de horas
        if self.hora_inicio and self.hora_final:
            # 1. Comprobamos que la hora final no sea anterior a la inicial
            if self.hora_final < self.hora_inicio:
                raise ValidationError({
                    'hora_final': 'La hora de finalización no puede ser anterior a la hora de inicio.'
                })


    class Meta:
        verbose_name = "Anexo V"
        verbose_name_plural = "Anexos V"
