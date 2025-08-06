from django.urls import path
from .views import UserDetailView, CustomPasswordChangeView
app_name = 'users'

urlpatterns = [
    path('detalle/<str:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]