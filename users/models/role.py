from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre del Rol')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

