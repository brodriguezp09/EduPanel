from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.text import slugify

from .role import Role 


class CustomUserManager(BaseUserManager):
    """
    Gestor personalizado para el modelo CustomUser donde el email o el slug son el identificador único.
    """
    def create_user(self, slug, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el slug, email y contraseña dados.
        """
        if not email:
            raise ValueError('El campo Email es obligatorio')
        if not slug:
            raise ValueError('El campo Slug es obligatorio')
            
        email = self.normalize_email(email)
        user = self.model(slug=slug, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, slug, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con el slug, email y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        # Asegurarnos de que los campos requeridos tienen un valor por defecto para el superusuario
        extra_fields.setdefault('username', slug)
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')

        return self.create_user(slug, email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el AbstractUser de Django.
    """
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False, verbose_name='Correo Electrónico')
    slug = models.SlugField(unique=True, max_length=100, editable=False)
    años_servicio = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)], verbose_name='Años de Servicio')
    dias_asuntos_propios_disfrutados = models.PositiveIntegerField(default=0, verbose_name='Días de Asuntos Propios Disfrutados')
    dias_asuntos_propios = models.PositiveIntegerField(default=0, editable=True, verbose_name='Días de Asuntos Propios Asignados')
    roles = models.ManyToManyField(Role, blank=True, verbose_name='Roles', related_name='users')

    # Asignamos el gestor personalizado
    objects = CustomUserManager()

    USERNAME_FIELD = 'slug'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        trienios = self.años_servicio // 3
        
        if trienios < 6:
            total_dias = 5
        
        # A partir del sexto trienio (18 años), se tiene un día más.
        total_dias = 6
        
        # A partir de ahí, un día más por cada 5 años adicionales de servicio.
        años_despues_sexto_trienio = self.años_servicio - 18
        if años_despues_sexto_trienio > 0:
            dias_adicionales = años_despues_sexto_trienio // 5
            total_dias += dias_adicionales
        
        self.dias_asuntos_propios = min(total_dias, 7)
        if not self.slug and self.email:
            self.slug = slugify(self.email.split('@')[0])
            
        super().save(*args, **kwargs)
