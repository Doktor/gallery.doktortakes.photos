from django.utils.timesince import timesince

import exifread
import os
# noinspection PyPep8Naming
from datetime import datetime as DT


def format_filesize(b):
    """Returns a human-readable string representation of a filesize, given
    the filesize in bytes."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(b) < 1024.0:
            return "%3.2f %s" % (b, unit)
        b /= 1024.0
    return "%.2f %s" % (b, 'TB')


# noinspection PyBroadException
def f_stop(f):
    """Returns the decimal equivalent of a fractional F-stop string."""
    try:
        f = f.split('/')
    except:
        return None
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return f[0]


def get_photo_info(photo):
    """Returns a list of tuples, containing EXIF data and other information for
    a photo."""
    photo.image.open()

    exif = exifread.process_file(photo.image.file)

    date_format = "%Y-%m-%d %H:%M:%S"

    info = [
        ("Camera", exif['Image Model'].printable),
        ("Lens", exif['EXIF LensModel'].printable),

        ("ISO", 'ISO ' + exif['EXIF ISOSpeedRatings'].printable),
        ("Focal length",
         exif['EXIF FocalLength'].printable + ' mm'),
        ("Aperture",
         'f/' + str(f_stop(exif['EXIF FNumber'].printable))),
        ("Flash", exif['EXIF Flash'].printable),
        ("Exposure time", exif['EXIF ExposureTime'].printable + ' s'),
        ("Exposure bias", exif['EXIF ExposureBiasValue'].printable),
        ("Exposure mode", exif['EXIF ExposureMode'].printable.lower()),
        ("Metering", exif['EXIF MeteringMode'].printable.lower()),

        ("Width", photo.width),
        ("Height", photo.height),
        ("File size", photo.filesize),
        ("File name", photo.filename),
        ("MD5 hash", photo.md5),

        ("Taken",
         "{datetime} ({relative} ago)".format(
             datetime=DT.strftime(photo.taken, date_format),
             relative=timesince(photo.taken))),

        ("Edited",
         "{datetime} ({relative} ago)".format(
             datetime=DT.strftime(photo.edited, date_format),
             relative=timesince(photo.edited))),
    ]

    photo.image.close()

    return info
