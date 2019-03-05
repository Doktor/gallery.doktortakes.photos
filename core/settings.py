import json
import os


# General settings
import sys

TEST = any('test' in argv for argv in sys.argv)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'django.txt'), 'r') as f:
    SECRET_KEY = f.read().strip()

DEBUG = not os.path.isfile(os.path.join(BASE_DIR, 'production'))

with open(os.path.join(BASE_DIR, 'data', 'allowed_hosts.txt')) as f:
    ALLOWED_HOSTS = f.read().strip().split('\n')

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'photos',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'auth', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

ENABLE_REGISTRATION = False

LOGIN_URL = 'log_in'


# Database

if not TEST:
    if DEBUG:
        filename = os.path.join(BASE_DIR, 'data', 'database_debug.json')
    else:
        filename = os.path.join(BASE_DIR, 'data', 'database.json')

    with open(filename) as f:
        default = json.loads(f.read())
else:
    default = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

DATABASES = {'default': default}


# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache/')
    }
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[{asctime}] {levelname} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
        'gunicorn': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'gunicorn'],
            'propagate': True,
        },
        # Standard requests
        'django.request': {
            'handlers': ['console_debug', 'gunicorn'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Requests when running the development server
        'django.server': {
            'handlers': ['console_debug'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['require_debug_true'],
        }
    }
}


# Security

if not DEBUG:
    SECURE_SSL_REDIRECT = True

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'D, Y-m-d'
DATETIME_FORMAT = 'D, Y-m-d H:i:s'

SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i:s'

from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"


# Static & media files

# Always store static files in local storage
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static.1')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Toggle local/remote storage for media files
if not TEST:
    LOCAL_STORAGE = False
else:
    LOCAL_STORAGE = True

MEDIA_URL = '/media/'

if LOCAL_STORAGE:
    if not TEST:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    else:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')
else:
    with open(os.path.join(BASE_DIR, 'data', 'aws.json')) as f:
        aws = json.loads(f.read())

    AWS_ACCESS_KEY_ID = aws['access']
    AWS_SECRET_ACCESS_KEY = aws['secret']
    AWS_STORAGE_BUCKET_NAME = aws['bucket']
    AWS_S3_ENDPOINT_URL = aws['endpoint']

    # Cache images for up to 14 days
    CACHE_CONTROL_MAX_AGE = 60 * 60 * 24 * 14

    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': f'max-age={CACHE_CONTROL_MAX_AGE}'}
    AWS_LOCATION = ''
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'

    DEFAULT_FILE_STORAGE = 'core.storages.MediaStorage'


# Task queue

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'US/Eastern'
