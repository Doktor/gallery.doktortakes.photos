from typing import Union

from django.conf import settings
from django.core.files import File
from django.core.files.storage import DefaultStorage, FileSystemStorage
from django.db.models.fields.files import ImageFieldFile

import hashlib
import os
import uuid
from datetime import datetime as DateTime
from io import BytesIO
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")

CHUNK_SIZE = 64 * 1024  # 64 KB
DATE_FORMAT = "%Y:%m:%d %H:%M:%S"


def format_file_size(b: float) -> str:
    for unit in ('B', 'KB', 'MB', 'GB'):
        if abs(b) < 1024.0:
            return "%3.2f %s" % (b, unit)
        b /= 1024.0
    return "%.2f %s" % (b, 'TB')


def generate_md5_hash(file: File) -> str:
    hasher = hashlib.md5()

    for chunk in file.chunks(chunk_size=CHUNK_SIZE):
        hasher.update(chunk)

    return hasher.hexdigest()


def get_modified_time_utc(file: Union[BytesIO, File]) -> DateTime:
    if isinstance(file, BytesIO):
        name = os.path.join(settings.BASE_DIR, 'temp', f'{uuid.uuid4()}.tmp')

        try:
            with open(name, 'wb') as f:
                f.write(file.read())
        except:
            return DateTime.now(tz=UTC)
        else:
            ts = os.path.getmtime(name)
            m_time = DateTime.fromtimestamp(ts).replace(tzinfo=UTC)
            os.remove(name)
            return m_time

    if isinstance(file, ImageFieldFile):
        storage = DefaultStorage()
    else:
        storage = FileSystemStorage()

    try:
        return storage.get_modified_time(file.name)
    except FileNotFoundError:
        return DateTime.now(tz=UTC)
