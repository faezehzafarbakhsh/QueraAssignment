"""
Django settings for QueraPyRate project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename=".env.main"))
IS_PRODUCTION = int(os.environ.get("IS_PRODUCTION"))

if IS_PRODUCTION:
    load_dotenv(find_dotenv(filename=".env.production"))
else:
    load_dotenv(find_dotenv(filename=".env.development"))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG"))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
DEFAULT_DATABASE_HOST = os.environ.get("DEFAULT_DATABASE_HOST")


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OTHER_APPS = [
    "rest_framework",
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_celery_results',

]

PROJECT_APPS = [
    'EduBase',
    'Identity',
    'EduTerm',
    'EduEnroll',
    'EduRequest',
]

INSTALLED_APPS = [*DJANGO_APPS, *OTHER_APPS, *PROJECT_APPS]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'QueraPyRate.urls'

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

WSGI_APPLICATION = 'QueraPyRate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DEFAULT_DATABASE_ENGINE"),
        'NAME': os.environ.get("DEFAULT_DATABASE_NAME"),
        'USER': os.environ.get("DEFAULT_DATABASE_USER"),
        'PASSWORD': os.environ.get("DEFAULT_DATABASE_PASSWORD"),
        'HOST': DEFAULT_DATABASE_HOST,
        'PORT': os.environ.get("DEFAULT_DATABASE_PORT"),
    },
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
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")
TIME_ZONE = os.environ.get("TIME_ZONE")
USE_I18N = os.environ.get("USE_I18N")
USE_L10N = os.environ.get("USE_L10N")
USE_TZ = os.environ.get("USE_TZ")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = os.environ.get("STATIC_URL")
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get("STATIC_ROOT_NAME"))
MEDIA_DIR = os.path.join(BASE_DIR, os.environ.get("MEDIA_DIR_NAME"))
MEDIA_URL = os.environ.get("MEDIA_URL")
MEDIA_ROOT = MEDIA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
USE_THOUSAND_SEPARATOR = int(os.environ.get("USE_THOUSAND_SEPARATOR"))
THOUSAND_SEPARATOR = os.environ.get("THOUSAND_SEPARATOR")
DECIMAL_SEPARATOR = os.environ.get("DECIMAL_SEPARATOR")
NUMBER_GROUPING = int(os.environ.get("NUMBER_GROUPING"))

AUTH_USER_MODEL = 'Identity.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10

}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# add your host of the email here in this case its Gmail so we are going to use Gmail host
EMAIL_HOST = 'smtp.gmail.com'
CELERY_RESULT_BACKEND = 'rpc://'
EMAIL_USE_TLS = True
# add the port number of the email server
EMAIL_PORT = 587
# add your gamil here
EMAIL_HOST_USER = 'quera0322@gmail.com@gmail.com'
# add your password here
EMAIL_HOST_PASSWORD = 'asdfgj79595'
DEFAULT_FROM_EMAIL = 'Celery quera0322@gmail.com'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Adjust the logging level as needed
    },
    'loggers': {
        'QueraPyRate': {
            'handlers': ['console'],
            'level': 'INFO',  # Adjust the logging level as needed
            'propagate': True,
        },
    },
}
