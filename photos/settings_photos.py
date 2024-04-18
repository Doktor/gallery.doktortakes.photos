from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime

import datetime
import json
import os


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


# Albums

ITEMS_PER_PAGE = 30
ITEMS_IN_FILMSTRIP = 11


# Thumbnails
EXTRA_SMALL_SQUARE_THUMBNAIL_WIDTH = 96  # 3840 / 40
SQUARE_THUMBNAIL_WIDTH = 400
MEDIUM_SQUARE_THUMBNAIL_WIDTH = 640  # 3840 / 6
LARGE_SQUARE_THUMBNAIL_WIDTH = 960   # 3840 / 4

MEDIUM_THUMBNAIL_SIZE = 1280  # 3840 / 3

THUMBNAIL_QUALITY = 80
