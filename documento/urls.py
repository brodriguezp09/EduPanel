from django.urls import path
from .views import DocumentoListView

app_name = 'documento'

urlpatterns = [
    path('', DocumentoListView.as_view(), name='documento_list'),
]