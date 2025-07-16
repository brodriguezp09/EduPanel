from django.urls import path
from .views import solicitar_permiso_view

app_name = 'asuntosParticulares'

urlpatterns = [
    path('solicitar/', solicitar_permiso_view, name='solicitar_permiso'),
]
