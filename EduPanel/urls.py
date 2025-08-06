from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', user_views.home, name='home'),
    path('asuntos_personales/', include('asuntosParticulares.urls')),
    path('documentos/', include('documento.urls')),
    path('usuario/', include('users.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
