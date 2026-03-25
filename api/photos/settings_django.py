import json
import os
import socket
import sys
import warnings
from django.core.management.utils import get_random_secret_key


def filter_none(list):
    return [item for item in list if item is not None]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# General settings
TEST = any('test' in argv for argv in sys.argv)
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

secret_key = os.environ.get('DJANGO_SECRET_KEY') or None

if secret_key is None:
    if DEBUG:
        secret_key = get_random_secret_key()

        if not TEST:
            warnings.warn("secret key not specified, creating a temporary key")
    else:
        print("secret key not specified, exiting", file=sys.stderr)
        sys.exit(1)

SECRET_KEY = secret_key

internal_ips = ['127.0.0.1', 'localhost']
allowed_hosts_comma_separated = os.environ.get('DJANGO_ALLOWED_HOSTS_COMMA_SEPARATED', '')

ALLOWED_HOSTS = [host for host in allowed_hosts_comma_separated.split(',') if host] or internal_ips
INTERNAL_IPS = internal_ips


# Application definition

INSTALLED_APPS = filter_none([
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'photos',
    'webpack_loader',
])

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
if DEBUG and not TEST:
    INSTALLED_APPS.append('debug_toolbar')

    _, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_METADATA_CLASS': None,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [],  # Use standard permissions
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

MIDDLEWARE = filter_none([
    'photos.middleware.ProfilerMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'photos.middleware.RequestLoggingMiddleware',
])

ROOT_URLCONF = 'photos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'photos', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'photos.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'photos.wsgi.application'

ENABLE_REGISTRATION = False

LOGIN_URL = 'log_in'


# Database

if TEST:
    default = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
else:
    default = {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
    }

DATABASES = {"default": default}


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


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
            'stream': sys.stdout,
        },
        'gunicorn': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_false'],
            'stream': sys.stdout,
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
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

# Local or remote storage for media files
LOCAL_STORAGE = os.environ.get('DJANGO_USE_LOCAL_STORAGE', 'true').lower() == 'true'

MEDIA_URL = '/media/'

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if LOCAL_STORAGE:
    if not TEST:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    else:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')
else:
    STORAGES["default"] = {
        "BACKEND": "photos.storage_backends.CustomS3Boto3Storage",
    }

    # Keys
    AWS_ACCESS_KEY_ID = os.environ.get('SPACES_ACCESS_KEY', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('SPACES_SECRET_KEY', '')

    # Region
    AWS_S3_USE_SSL = True
    AWS_S3_REGION_NAME = os.environ.get('SPACES_REGION_NAME', '')
    AWS_S3_ENDPOINT_URL = os.environ.get('SPACES_ENDPOINT', '')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('SPACES_CUSTOM_DOMAIN', '')

    # Bucket
    AWS_STORAGE_BUCKET_NAME = os.environ.get('SPACES_BUCKET_NAME', '')
    AWS_LOCATION = os.environ.get('SPACES_PATH_PREFIX', '')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_ADDRESSING_STYLE = 'virtual'

    # Cache images for up to 14 days
    CACHE_CONTROL_MAX_AGE = 60 * 60 * 24 * 14
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': f'max-age={CACHE_CONTROL_MAX_AGE}'}

    S3_NETWORK_TIMEOUT_SECONDS = 5
    S3_NETWORK_RETRY_COUNT = 2


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '',
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'STATS_FILE': os.path.join(BASE_DIR, 'static', 'webpack-stats.json'),
    }
}
