from django.core.files.storage import DefaultStorage

import hashlib

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
    storage = DefaultStorage()
    return storage.get_modified_time(file.name)
