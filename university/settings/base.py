import os
from unipath import Path
BASE_DIR = Path(__file__).ancestor(3)
SECRET_KEY = 'django-insecure-b1bup^#9zvon$%$ig+=nrapx3atp^_=ykk6q(n#k6+m=$)7==o'
SECRET_KEY_TOKEN = '9zvon$%$ig+=nrapx3atp^_=ykk6q(n#k6+m'
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
APPS_LOCAL = [
    'apps.user',
    'apps.system',
    'apps.equipo'
]
THY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + APPS_LOCAL+ THY_APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'university.urls'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.user'
AUTH_AUTHENTICATION_TYPE="email"
LOGIN_URL = '/'
# Hubicación del modelos user para las procesos de autenticación de usuarios.
# AUTH_USER_MODEL = 'usuario.user'
# STATIC_ROOT = "staticfiles"

# Path de hubicación para la carpeta de los templates
TEMPLATE_DIRS= [BASE_DIR.child("templates")]


# Hubicación url para los archivos estaticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Path de hubicacion para la carpeta static delos archivos estaticos
STATIC_FILES = [BASE_DIR.child('static')]


# Path de hubicacion para la carpeta static delos archivos estaticos 
# para la variable de configuración STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR.child('static')]


# Dirección url general para los archivos multimedia
MEDIA_URL = '/media/'


# Path de hubicación para los archivos multimedia
MEDIA_ROOT = BASE_DIR.child('media')

CORS_ALLOW_ALL_ORIGINS: True


ALGORITM_ENCAP_BACK = "RS256"