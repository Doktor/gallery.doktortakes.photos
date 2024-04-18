from django.core.files import File

from photos.models.photo.photo import COLOR_NONE, COLOR_WHITE, COLOR_BLACK
from photos.utils.models import DATE_FORMAT, get_modified_time_utc

import datetime
import exifread
import pytz
from lxml import etree

strptime = datetime.datetime.strptime

XMP_START = b'<x:xmpmeta'
XMP_END = b'</x:xmpmeta>'

NS = {
    'x': "adobe:ns:meta/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'xmp': "http://ns.adobe.com/xap/1.0/"
}


def parse_exif_data(photo: 'Photo', file: File) -> None:
    """Extracts EXIF data from an image and adds it to a Photo object."""

    file.seek(0)
    raw_exif = exifread.process_file(file, details=False, debug=False)
    photo.exif = {k: v.printable for k, v in raw_exif.items()}

    # Timestamps
    modified = get_modified_time_utc(file)
    tz = pytz.utc

    taken = photo.exif.get('EXIF DateTimeOriginal', None)
    if taken is not None:
        photo.taken = strptime(taken, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.taken = modified

    edited = photo.exif.get('Image DateTime', None)
    if edited is not None:
        photo.edited = strptime(edited, DATE_FORMAT).replace(tzinfo=tz)
    else:
        photo.edited = modified


def parse_xmp_data(photo: 'Photo', file: File) -> None:
    """Extracts XMP data from an image and adds it to a Photo object."""
    return

    # file.seek(0)
    # data = file.read()
    # start = data.find(XMP_START)
    # end = data.find(XMP_END)
    #
    # if start == -1 or end == -1:
    #     pass
    # else:
    #     xml = data[start:end + len(XMP_END)].decode('utf-8')
    #     root = etree.fromstring(xml)
    #     element = root.xpath('.//rdf:Description', namespaces=NS)[0]
    #     label = element.xpath('@xmp:Label', namespaces=NS)[0].lower()


def format_f_stop(f: str) -> float:
    """Takes an f-stop as a fractional string and converts it to a number."""
    try:
        f = f.split('/')
    except AttributeError:
        return 0
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return float(f[0])


def get_exif(photo: 'Photo') -> dict:
    e = photo.exif

    if not e:
        return {}

    camera = e.get('Image Model', 'Camera unknown')

    lens_make = e.get('EXIF LensMake', e.get('Image Make', None))
    lens_model = e.get('EXIF LensModel', None)

    if lens_model is None:
        lens = 'Lens unknown'
    elif lens_model.lower().startswith('tamron'):
        lens = 'Tamron' + lens_model[len('Tamron'):]
    else:
        if lens_make is None:
            lens = lens_model
        else:
            lens = f'{lens_make} {lens_model}'

        if 'EF-S' in lens:
            lens = lens.replace('EF-S', 'EF-S ')
        elif 'EF' in lens:
            lens = lens.replace('EF', 'EF ')

    try:
        focal_length = f"{e['EXIF FocalLength']} mm"
    except KeyError:
        focal_length = 'Unknown'

    try:
        shutter_speed = f"{e['EXIF ExposureTime']} s"
    except KeyError:
        shutter_speed = 'Unknown'

    try:
        f_stop = f"f/{format_f_stop(e['EXIF FNumber'])}"
    except KeyError:
        if camera != 'Camera unknown':
            f_stop = 'f/0'
        else:
            f_stop = 'Unknown'

    try:
        iso_speed = f"ISO {e['EXIF ISOSpeedRatings']}"
    except KeyError:
        iso_speed = 'Unknown'

    return {
        'camera': camera,
        'lens': lens,
        'focal_length': focal_length,
        'shutter_speed': shutter_speed,
        'aperture': f_stop,
        'iso_speed': iso_speed,
    }
