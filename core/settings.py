import json
import os


# General settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'data', 'django.txt'), 'r') as f:
    SECRET_KEY = f.read().strip()

DEBUG = not os.path.isfile(os.path.join(BASE_DIR, 'production'))

with open(os.path.join(BASE_DIR, 'data', 'allowed_hosts.txt')) as f:
    ALLOWED_HOSTS = f.read().strip().split('\n')


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

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'photos.db'),
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
STATIC_URL = '/static/'

# Toggle local/remote storage for media files
LOCAL_STORAGE = True

if LOCAL_STORAGE:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
else:
    with open(os.path.join(BASE_DIR, 'data', 'aws.json')) as f:
        aws = json.loads(f.read())

    AWS_ACCESS_KEY_ID = aws['access']
    AWS_SECRET_ACCESS_KEY = aws['secret']
    AWS_STORAGE_BUCKET_NAME = aws['bucket']
    AWS_S3_ENDPOINT_URL = aws['endpoint']

    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_LOCATION = ''
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'

    DEFAULT_FILE_STORAGE = 'core.storages.MediaStorage'
    MEDIA_URL = '/media/'
