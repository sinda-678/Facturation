from pathlib import Path
import os

# Configuration de base du répertoire
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemin vers les fichiers de templates
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Chemin vers les fichiers statiques
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

# Chemin vers les fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
try:
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG : 'alert-info',
        messages.INFO : 'alert-info',
        messages.SUCCES :  'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR : 'alert-darger'
    }
except Exception as e:
    pass
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=z6n9p$s+m@h=!!&c90i5w6n$x)wp2iu1tl@(bij$1yrf^hsv$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fact_app',  # Ajoutez ici les applications spécifiques à votre projet
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_invoice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],  # Utilisation du TEMPLATES_DIR ici
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

WSGI_APPLICATION = 'django_invoice.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
from django.utils.translation import gettext_lazy as _
LANGUAGE = [
    ('fr', _('French')),
    ('en'), _('English'),
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Configuration des fichiers statiques supplémentaires
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
