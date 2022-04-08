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
SQUARE_THUMBNAIL_WIDTH = 400
THUMBNAIL_QUALITY = 80


# Watermarks
WATERMARK_OFFSET_PERCENT = 5 / 6


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
