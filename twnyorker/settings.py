"""
Django settings for twnyorker project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import os
import dj_database_url
import django_heroku
from google.oauth2 import service_account
import json

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'blog.apps.BlogConfig',
    'club.apps.ClubConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'twnyorker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'twnyorker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {}
if env('TWNYORKER_RUNLOCAL') == 'True':
    DATABASES['default'] = env.db('DATABASE_URL')
else:
    DATABASES['default'] = dj_database_url.config()

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

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static'),
    os.path.join(PROJECT_ROOT, 'static'),
)

if env('TWNYORKER_RUNLOCAL') == 'True':
    MEDIA_URL = '/media/'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    MEDIA_URL = 'https://storage.googleapis.com/storage/'
    DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
    STATICFILES_STORAGE = env('STATICFILES_STORAGE')
    GS_PROJECT_ID = env('GS_PROJECT_ID')
    GS_BUCKET_NAME = env('GS_BUCKET_NAME')

    # Reference: https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku/62536750#62536750
    # the json credentials stored as env variable
    json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    # generate json - if there are errors here remove newlines in .env
    json_data = json.loads(json_str)
    # the private_key needs to replace \n parsed as string literal with escaped newlines
    json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')

    # use service_account to generate credentials object
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(json_data)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

AUTH_USER_MODEL = 'account.SiteUser'

# AUTHENTICATION_BACKENDS = ['account.backends.EmailBackend']
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ["Format", "Styles", "FontSize"],
            ["Bold", "Italic", "Underline", "Strike", "SpellChecker", 'Undo', "Image", "Table", "Link", "Unlink"],
            ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ],
        'resize_enabled': False,
        'skin': 'moono',
        'height': 420,
        'width': '100%',
    }
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

# Activate Django-Heroku.
django_heroku.settings(locals())
del DATABASES['default']['OPTIONS']['sslmode']
