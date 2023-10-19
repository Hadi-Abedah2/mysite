"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%g_7okh1qlkg@64(kvcqsutjixo@(!=#u^jj7@mrm6i24p*8x-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['hadiabedah2.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ads",
    "home",
    'crispy_forms',
    'crispy_bootstrap4',
    'taggit',
    'widget_tweaks',
    'django_extensions' ,
    'django.contrib.humanize',
    # this for google social login
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_gravatar',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


#from decouple import config
#db_password = config('db_password')
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',          #DB config for my local host
#        'NAME': 'mysite',
#        'USER': 'postgres',
#        'PASSWORD': db_password,
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}
from decouple import config
db_password = config('db_password')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',          #DB config for pythonanywhere
        'NAME': 'hadiabedah2$default',
        'USER': 'hadiabedah2',
        'PASSWORD': db_password,
        'HOST': 'hadiabedah2.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

import os
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

#STATICFILES_DIRS = [os.path.join(BASE_DIR,"mysite", "static"),] # for local
STATICFILES_DIRS = [os.path.join(BASE_DIR,"mysite", "mysite", "static"),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

TAGGIT_CASE_INSENSITIVE = True

# this for google social login

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True


from decouple import config

SECRET_KEY = config('SECRET_KEY') #using python-decouple and environment variables to make my project secure
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '284782358202-k64aqapbsfvh1nano39r4k9hb0hvjgj7.apps.googleusercontent.com',
            'secret': SECRET_KEY,
        }
    }
}


GRAVATAR_DEFAULT_IMAGE = 'mm'
GRAVATAR_SECURE_REQUESTS = True