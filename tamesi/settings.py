"""
Django settings for tamesi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY', '')

if not SECRET_KEY:
    try:
        with open('secret_key', 'r') as key:
            SECRET_KEY = key.read().strip()
    except:
        pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    'tamesi.herokuapp.com',
    '188.226.203.68',
    'tamesi.info',
    'www.tamesi.info'
]


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'storages',
    # 'collectfast',
    'saiban'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tamesi.urls'

WSGI_APPLICATION = 'tamesi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

import dj_database_url
DATABASES = {
    "default": dj_database_url.config(default='postgres://localhost'),
}

# DATABASES['default'] =  dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'client/static_collected'
MEDIA_ROOT = 'uploads'

STATICFILES_DIRS = (
    # build task: grunt compiles everything (including bower_components) here
    'client/static',
)

# Additional configuration for admin backend
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Configuration for register module
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 1

# Log to STDERR
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

# Try to import local settings (if any)
if os.environ.get('DEPLOY') is None:
    try:
        from local_settings import *
    except ImportError:
        pass

# Try to import deploy setting if appropriate OS vairable is set
if os.environ.get('DEPLOY') is not None:
    try:
        from deploy_settings import *
    except ImportError:
        pass

# Serve static files from Amazon S3 bucket
if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    #S3_URL = 'https://s3-us-west-2.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    #STATICFILES_STORAGE = "require_s3.storage.OptimizedCachedStaticFilesStorage"
    AWS_PRELOAD_METADATA = True

    '''
    AWS_HEADERS = {
        "Cache-Control": "public, max-age=86400",
    }
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SECURE_URLS = True
    AWS_REDUCED_REDUNDANCY = False
    AWS_IS_GZIPPED = False
    '''
