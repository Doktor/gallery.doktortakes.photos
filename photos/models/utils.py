from django.conf import settings
from django.core.files.storage import DefaultStorage, FileSystemStorage
from django.db.models.fields.files import ImageFieldFile

import hashlib
import os
import uuid
from io import BytesIO

CHUNK_SIZE = 64 * 1024  # 64 KB
DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


def format_file_size(b):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if abs(b) < 1024.0:
            return "%3.2f %s" % (b, unit)
        b /= 1024.0
    return "%.2f %s" % (b, 'TB')


def generate_md5_hash(file):
    hasher = hashlib.md5()

    for chunk in file.chunks(chunk_size=CHUNK_SIZE):
        hasher.update(chunk)

    return hasher.hexdigest()


def get_modified_time_utc(file):
    if isinstance(file, ImageFieldFile):
        storage = DefaultStorage()
    else:
        storage = FileSystemStorage()

        if isinstance(file, BytesIO):
            name = os.path.join(settings.BASE_DIR, 'temp', f'{uuid.uuid4()}.tmp')

            try:
                with open(name, 'wb') as f:
                    f.write(file.read())
            except:
                return None
            else:
                m_time = storage.get_modified_time(name)
                os.remove(name)
                return m_time

    return storage.get_modified_time(file.name)
