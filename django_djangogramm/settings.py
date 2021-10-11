"""
Django settings for django_djangogramm project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

import dj_database_url
import django_heroku
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h+gmizelv*h)(y1ua)qa5f3z4bq%4jz%(-*)**%h$1pw-c2ibz'
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-h+gmizelv*h)(y1ua)qa5f3z4bq%4jz%(-*)**%h$1pw-c2ibz')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = ['https://evening-reef-96678.herokuapp.com/', '127.0.0.1', 'localhost', 'testserver']

# Application definition

INSTALLED_APPS = [
    'djangogramm.apps.DjangogrammConfig',
    'bootstrap5',
    'django_cleanup',
    'easy_thumbnails',
    'cloudinary',
    # 'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_djangogramm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'django_djangogramm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangogramm',
        'USER': 'dg',
        'PASSWORD': 'm091278mm',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# use heroku postgres db
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# add custom user model
AUTH_USER_MODEL = 'djangogramm.DgUser'
# AUTHENTICATION_BACKENDS = ['djangogramm.authentication.EmailBackend']

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login
LOGIN_REDIRECT_URL = '/'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'small': {
            'size': (64, 64),
            'crop': 'smart',
        },
        'default': {
            'size': (96, 96),
            'crop': 'scale',
        },
        'large': {
            'size': (256, 256),
            'crop': 'scale',
        },
    },
}
THUMBNAIL_BASEDIR = 'thumbnails'

# email settings
EMAIL_PORT = 1025

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# Activate Django-Heroku.
django_heroku.settings(locals())

# cloudinary config
cloudinary.config(
    cloud_name="dsg2wylkr",
    api_key="678435832967774",
    api_secret="W_jvzN7oLyYWqAAKdD8hofhnVoo"
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
