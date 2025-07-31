# users/admin.py

import csv
import io
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.text import slugify
from django.contrib import messages

from .models import CustomUser, Role, Horario, Asignatura
from .forms import CargaMasivaForm

class CustomUserAdmin(UserAdmin):
    # Redefinimos 'fieldsets' para evitar duplicados y tener una estructura limpia.
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Información Personal', {"fields": ("first_name", "last_name", "email", "slug")}),
        ('Datos Laborales', {'fields': ('años_servicio', 'dias_asuntos_propios', 'dias_asuntos_propios_disfrutados')}),
        ('Roles y Permisos', {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "roles",
                "groups",
                "user_permissions",
            ),
        }),
        ('Important dates', {"fields": ("last_login", "date_joined")}),
    )

    # Reorganizamos 'add_fieldsets' para la página de creación de usuario.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2'),
        }),
        ('Información Personal y Laboral', {
            'fields': ('first_name', 'last_name', 'años_servicio'),
        }),
    )
    
    list_display = ('username', 'slug', 'email', 'first_name', 'last_name', 'is_staff')
    readonly_fields = ( 'slug',)
    filter_horizontal = ('groups', 'user_permissions', 'roles')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CargaMasivaForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'El fichero no es un CSV')
                    return redirect("..")

                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.reader(io_string, delimiter=';')
                    next(reader) 

                    docente_role, created = Role.objects.get_or_create(name='Docente')
                    
                    usuarios_creados = 0
                    for row in reader:
                        # Leemos la fila del CSV
                        nombre_csv, apellidos_csv, email, años_servicio, dni = row
                        slug = slugify(email.split('@')[0])
                        username = slug
                        
                        # Mapeamos los datos del CSV a los campos correctos del modelo
                        user, created = CustomUser.objects.get_or_create(
                            email=email,
                            defaults={
                                'username': username,
                                'slug': slug,
                                'first_name': nombre_csv,
                                'last_name': apellidos_csv,
                                'años_servicio': int(años_servicio),
                            }
                        )
                        if created:
                            user.set_password(dni) # Usamos el DNI como contraseña
                            user.roles.add(docente_role)
                            user.save()
                            usuarios_creados += 1

                    messages.success(request, f"Se han importado y creado {usuarios_creados} usuarios nuevos.")
                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al procesar el fichero: {e}")

                return redirect("..")
        
        form = CargaMasivaForm()
        payload = {"form": form}
        payload.update(self.admin_site.each_context(request))

        return render(request, "admin/csv_form.html", payload)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registramos el modelo Horario con la funcionalidad de importación
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'dia', 'hora', 'asignatura')
    list_filter = ('profesor', 'dia', 'asignatura')
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-horario-csv/', self.import_csv, name='users_horaio_import'),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CargaMasivaForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'El fichero no es un CSV')
                    return redirect("..")

                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.reader(io_string, delimiter=';')
                    next(reader) # Saltar la cabecera

                    horarios_creados = 0
                    for row in reader:
                        profesor_slug, asignatura_nombre, dia, hora = row
                        
                        # Obtener los objetos relacionados
                        profesor = CustomUser.objects.get(slug=profesor_slug)
                        asignatura, created = Asignatura.objects.get_or_create(nombre=asignatura_nombre)

                        # Crear o actualizar la franja horaria
                        horario, created = Horario.objects.update_or_create(
                            profesor=profesor,
                            dia=dia,
                            hora=hora,
                            asignatura=asignatura
                        )
                        if created:
                            horarios_creados += 1
                            
                    messages.success(request, f"Se han importado y creado {horarios_creados} nuevas franjas horarias.")
                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al procesar el fichero: {e}")

                return redirect("..")
        
        form = CargaMasivaForm()
        payload = {"form": form, "title": "Importar Horarios desde CSV"}
        payload.update(self.admin_site.each_context(request))

        return render(request, "admin/csv_form.html", payload)
