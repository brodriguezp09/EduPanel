from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
]
# Third-party apps
INSTALLED_APPS += [
    'tailwind',
    'theme',
    'django_browser_reload',
]
# Custom apps
INSTALLED_APPS += [
    'users.apps.UsersConfig',
    'asuntosParticulares.apps.AsuntosparticularesConfig',
#    'ausencias.apps.AusenciasConfig',
    'documento.apps.DocumentoConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'EduPanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EduPanel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] 
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]
JAZZMIN_SETTINGS = {
    "site_title": "Portal I.E.S Albarregas",
    "site_header": "IES. Albarregas",
    "site_brand": "Admin IES. Albarregas",
    
    "user_avatar": None,
    "show_recent_actions": False, 
    
    
    #############
    # Side Menu #
    #############    
    "show_sidebar": True,
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    
    "custom_links": {
    
        "asuntosparticulares":[{
            "name": "Solicitudes Pendientes",
            "url": "admin:informe_permisos",
            "icon": "fas fa-list-check",
           # "permissions": ["asuntosParticulares.view_asuntosparticulares"]
        },
        {
            "name": "Solicitudes Totales",
            "url": "admin:informe_permisos_totales",
            "icon": "fas fa-file-lines",
           # "permissions": ["asuntosParticulares.view_asuntosparticulares"]
        }
        ],

    },

    "icons": {
        "auth": "fas fa-users-cog",
        "users.CustomUser": "fas fa-user",
        "users.Asignatura": "fas fa-book",
        "users.Horario": "fas fa-clock",
        "users.Role": "fas fa-users-cog",
        "asuntosParticulares.AsuntosParticulares": "fas fa-umbrella-beach",
        "asuntosParticulares.DiaFestivo": "fas fa-calendar-check",
        "documento.CategoriaDocumento": "fas fa-folder",
        "documento.PlantillaDocumento": "fas fa-file-alt",
        
    },
    "copyright": "I.E.S Albarregas",
    "show_powered_by": False,
    
}

JAZZMIN_UI_TWEAKS = {
   "navbar_fixed": True,      
    "sidebar_fixed": True,    
    "footer_fixed": False, 
}

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')