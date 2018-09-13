from django.conf import settings

import os
import PIL.Image


# Media files

MEDIA_FOLDERS = {
    'ORIGINAL': 'original',
    'DISPLAY': 'photos',
    'THUMBNAIL': 'thumbs',
    'SQUARE': 'squares',
}

PANORAMAS_FOLDER = 'panoramas'
PANORAMA_THUMBNAILS_FOLDER = os.path.join('panoramas', 'thumbs')

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

COLOR_NONE = ''
COLOR_WHITE = 'w'
COLOR_BLACK = 'b'

COLOR_CHOICES = (
    (COLOR_NONE, 'None'),
    (COLOR_WHITE, 'White'),
    (COLOR_BLACK, 'Black'),
)

WATERMARKS_PATH = os.path.join(settings.BASE_DIR, 'data', 'watermarks')

WATERMARK_IMAGES = {}

if WATERMARKS_ENABLED:
    for size in (2400, 3600):
        for color in ('black', 'white'):
            path = os.path.join(WATERMARKS_PATH, str(size), color + '.png')

            image = PIL.Image.open(path, 'r').convert('RGBA')
            key = (size, color[0])
            WATERMARK_IMAGES[key] = image

WATERMARK_OFFSET = 30
