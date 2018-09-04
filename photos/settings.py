from django.conf import settings

import os
import PIL.Image


# Media files

MEDIA_FOLDERS = {
    'ORIGINAL': 'photos',
    'DISPLAY': 'display',
    'THUMBNAIL': 'thumbs',
    'SQUARE': 'squares',
}

PANORAMAS_FOLDER = 'panoramas'
PANORAMA_THUMBNAILS_FOLDER = 'panoramas/thumbs'

DEFAULT_PATH = 'all'

# Index page

INDEX_ALBUMS = 12
INDEX_FEATURED_PHOTOS = 30

TAGLINES_PATH = os.path.join(settings.BASE_DIR, 'data', 'taglines.txt')

if os.path.isfile(TAGLINES_PATH):
    with open(TAGLINES_PATH, encoding='utf8') as f:
        TAGLINES = f.read().strip().split('\n')
else:
    TAGLINES = []


# Albums

ITEMS_PER_PAGE = 30
ITEMS_IN_FILMSTRIP = 11


# Display images

LONG, SHORT = 2400, 1600
LANDSCAPE_SIZE = (LONG, SHORT)
PORTRAIT_SIZE = (SHORT, LONG)


# Watermarks

WATERMARKS_ENABLED = getattr(settings, 'WATERMARKS_ENABLED', True)

WATERMARK_COLOR_NONE = ''
WATERMARK_COLOR_WHITE = 'w'
WATERMARK_COLOR_BLACK = 'b'

WATERMARKS_PATH = os.path.join(settings.BASE_DIR, 'data', 'watermarks')

if WATERMARKS_ENABLED:
    BLACK_PATH = os.path.join(WATERMARKS_PATH, 'black.png')
    BLACK_2400 = PIL.Image.open(BLACK_PATH, 'r').convert('RGBA')
    BLACK_2400.load()

    WHITE_PATH = os.path.join(WATERMARKS_PATH, 'white.png')
    WHITE_2400 = PIL.Image.open(WHITE_PATH, 'r').convert('RGBA')
    WHITE_2400.load()
else:
    BLACK_2400 = None
    WHITE_2400 = None

WATERMARK_OFFSET = 30

WATERMARK_COLOR_CHOICES = (
    (WATERMARK_COLOR_NONE, 'None'),
    (WATERMARK_COLOR_WHITE, 'White'),
    (WATERMARK_COLOR_BLACK, 'Black'),
)

WATERMARK_IMAGES = {
    WATERMARK_COLOR_WHITE: WHITE_2400,
    WATERMARK_COLOR_BLACK: BLACK_2400,
    WATERMARK_COLOR_NONE: WHITE_2400,
}

