"""
Django settings for kiite_me project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
#import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f+9()w&%ysda358ia+zkk)yxvrh2#v_6-7!*rr+w0nj3e319x9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] 

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'km',
    'django_filters',
    'widget_tweaks',
    'storages',
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

ROOT_URLCONF = 'kiite_me.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'kiite_me.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# 'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',    <= default, i changed it to postgresql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#for static pics------------------------------------
STATICFILES_DIRS = [ os.path.join(BASE_DIR,"static") ]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

#for profile pics------------------------------------
MEDIA_URL = '/images/profile_images/'
MEDIA_ROOT = os.path.join(BASE_DIR,'staticfiles/images/profile_images')

#SMTP configuration FOR SENDING PASSWORD RESET EMAIL(you can search by 'google sntp configuration')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '**********'
EMAIL_HOST_PASSWORD = '**********'

AWS_ACCESS_KEY_ID = '**********'
AWS_SECRET_ACCESS_KEY = '**********'

AWS_STORAGE_BUCKET_NAME = '**********'
AWS_S3_FILE_OVERWRITE = '**********'
AWS_LOCATION = '**********'

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AUTH_USER_MODEL = 'km.CustomUser'
TEMP = os.path.join(BASE_DIR, 'temp')
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760