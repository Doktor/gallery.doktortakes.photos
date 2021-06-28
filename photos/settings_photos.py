from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime

import datetime
import json
import os
import PIL.Image


# Media files

MEDIA_FOLDERS = {
    'ORIGINAL': 'original',
    'DISPLAY': 'photos',
    'THUMBNAIL': 'thumbs',
    'SQUARE': 'squares',
}

DEFAULT_PATH = 'all'


# Index page

INDEX_ALBUMS = 12
INDEX_FEATURED_PHOTOS = 30

TAGLINES = settings.CONFIG['photos'].get('taglines', [])


# Albums

ITEMS_PER_PAGE = 30
ITEMS_IN_FILMSTRIP = 11


# Display images

CHECK_MINIMUM_SIZE = True
MINIMUM_LONG_EDGE, MINIMUM_SHORT_EDGE = 2400, 1600
LANDSCAPE_SIZE = (MINIMUM_LONG_EDGE, MINIMUM_SHORT_EDGE)
PORTRAIT_SIZE = (MINIMUM_SHORT_EDGE, MINIMUM_LONG_EDGE)


# Thumbnails
SQUARE_THUMBNAIL_SIZE = (400, 400)
THUMBNAIL_QUALITY = 80


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

    DEFAULT_WATERMARK = WATERMARK_IMAGES[(2400, 'w')]

WATERMARK_OFFSET = 30


# Changelog
GIT_STATUS_PATH = os.path.join(settings.BASE_DIR, 'data', 'git.json')

if os.path.isfile(GIT_STATUS_PATH):
    with open(GIT_STATUS_PATH, encoding='utf8') as f:
        data = json.loads(f.read().strip())

        data['last_commit_naturaltime'] = naturaltime(
            datetime.datetime.strptime(data['last_commit_datetime'], "%Y-%m-%d %H:%M:%S"))

        GIT_STATUS = data
else:
    GIT_STATUS = None
