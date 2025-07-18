from django.urls import path
from .views import solicitar_permiso_view,cancelar_solicitud_view, MisSolicitudesView, cancelar_solicitud_confirm_view

app_name = 'asuntosParticulares'

urlpatterns = [
    path('solicitar/', solicitar_permiso_view, name='solicitar_permiso'),
    path('mis-solicitudes/', MisSolicitudesView.as_view(), name='mis_solicitudes'),
    path('cancelar/<int:pk>/confirm/', cancelar_solicitud_confirm_view, name='cancelar_solicitud_confirm'),
    path('cancelar/<int:pk>/', cancelar_solicitud_view, name='cancelar_solicitud'),
]
