import os
import PIL.Image


# General settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'keys', 'django.txt'), 'r') as f:
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


# Password validation

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


# Static files

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'


# Display images & watermarks

LONG, SHORT = 2400, 1600
LANDSCAPE_SIZE = (LONG, SHORT)
PORTRAIT_SIZE = (SHORT, LONG)

WHITE = 'w'
BLACK = 'b'

WATERMARKS = (
    (WHITE, 'White'),
    (BLACK, 'Black'),
)

WATERMARKS_PATH = os.path.join(BASE_DIR, 'data', 'watermarks')
WATERMARK_OFFSET = 30

BLACK_PATH = os.path.join(WATERMARKS_PATH, 'black.png')
BLACK_2400 = PIL.Image.open(BLACK_PATH, 'r').convert('RGBA')
BLACK_2400.load()

WHITE_PATH = os.path.join(WATERMARKS_PATH, 'white.png')
WHITE_2400 = PIL.Image.open(WHITE_PATH, 'r').convert('RGBA')
WHITE_2400.load()

WATERMARK_IMAGES = {
    BLACK: BLACK_2400,
    WHITE: WHITE_2400,
    None: WHITE_2400,
}


# Media file locations

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ORIGINAL_IMAGES_FOLDER = 'photos'
DISPLAY_IMAGES_FOLDER = 'display'
THUMBNAILS_FOLDER = 'thumbs'
SQUARES_FOLDER = 'squares'

PANORAMAS_FOLDER = 'panoramas'
PANORAMA_THUMBNAILS_FOLDER = 'panoramas/thumbs'

DEFAULT_PATH = 'all'

# Index page

INDEX_ALBUMS = 12
INDEX_FEATURED_PHOTOS = 30

with open(os.path.join(BASE_DIR, 'data/taglines.txt'), encoding='utf8') as f:
    TAGLINES = f.read().strip().split('\n')


# Albums

ITEMS_PER_PAGE = 30
ITEMS_IN_FILMSTRIP = 11
