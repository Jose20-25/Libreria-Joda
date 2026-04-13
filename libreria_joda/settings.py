from pathlib import Path
import dj_database_url
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-8=elw)5_2sqc)a_e^-vuru0w%rctn6_ls689!htl6omkrglkv_')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Cloud Run agrega automáticamente el dominio .run.app
CLOUDRUN_SERVICE_URL = config('CLOUDRUN_SERVICE_URL', default='')
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS += [CLOUDRUN_SERVICE_URL.replace('https://', '').replace('http://', '')]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'libreria_joda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tienda.context_processors.categorias_nav',
            ],
        },
    },
]

WSGI_APPLICATION = 'libreria_joda.wsgi.application'


# Base de datos — SQLite local, PostgreSQL en producción
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=config('DB_SSL', default=False, cast=bool),
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Firebase
FIREBASE_STORAGE_BUCKET = config('FIREBASE_STORAGE_BUCKET', default='tiendajoda-c73c4.firebasestorage.app')
FIREBASE_SERVICE_ACCOUNT_PATH = BASE_DIR / 'firebase-service-account.json'

# Almacenamiento de imágenes: Firebase en producción, local en desarrollo
if config('FIREBASE_SERVICE_ACCOUNT_JSON', default='') or (BASE_DIR / 'firebase-service-account.json').exists():
    DEFAULT_FILE_STORAGE = 'tienda.firebase_storage.FirebaseStorage'
    MEDIA_URL = f'https://storage.googleapis.com/{FIREBASE_STORAGE_BUCKET}/media/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguridad en producción
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
