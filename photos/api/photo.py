from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET

from photos.models import Photo
from photos.settings import ITEMS_PER_PAGE
from photos.views import get_album_by_path

from pytz import timezone

from .utils import APIError, get_photo_from_request


def f_stop(f):
    try:
        f = f.split('/')
    except AttributeError:
        return None
    else:
        if len(f) == 2:
            return int(f[0]) / int(f[1])
        else:
            return f[0]


def get_exif(p):
    e = p.exif

    model = e['EXIF LensModel']

    if 'EF-S' in model:
        model = model.replace('EF-S', 'EF-S ')
    elif 'EF' in model:
        model = model.replace('EF', 'EF ')

    return {
        'camera': e['Image Model'],
        'lens': f"{e.get('EXIF LensMake', e['Image Make'])} "
                f"{model}",
        'shutter_speed': f"{e['EXIF ExposureTime']}s",
        'aperture': f"f/{f_stop(e['EXIF FNumber'])}",
        'iso_speed': f"ISO {e['EXIF ISOSpeedRatings']}",
    }


def generate_photo_dict(photo, index=None):
    taken = photo.taken.astimezone(timezone(photo.album.timezone))

    if index is not None:
        pass
    else:
        photos = photo.album.photos.all().order_by('taken')

        for i, item in enumerate(photos):
            if item.md5 == photo.md5:
                index = i
                break
        else:
            raise RuntimeError

    return {
        'image_url': photo.image.url,
        'thumbnail_url': photo.thumbnail.url,
        'square_thumbnail_url': photo.square_thumbnail.url,
        'url': photo.get_absolute_url(),
        'metadata': {
            'index': index,
            'taken': taken.strftime("%A, %Y-%m-%d, %-I:%M:%S %p"),
            'width': photo.width,
            'height': photo.height,
            'md5': photo.md5,
            'new_tab': photo.image.url,
            'download': reverse(
                'download', args=[photo.get_path(), photo.md5]),
        },
        'exif': get_exif(photo)
    }


def photo_to_response(photo):
    return JsonResponse(generate_photo_dict(photo))


class PhotoView(View):
    def get(self, request, *args, **kwargs):
        try:
            photo = get_photo_from_request(request)
        except APIError as e:
            return e.to_response()

        return photo_to_response(photo)

    @method_decorator(login_required)
    def delete(self, request, *args, **kwargs):
        try:
            photo = get_photo_from_request(request)
        except APIError as e:
            return e.to_response()

        try:
            photo.thumbnail.delete(save=False)
            photo.image.delete(save=False)
            photo.delete()

            return JsonResponse({
                'success': True,
                'message': "Photo deleted successfully.",
            })

        except (IOError, OSError):
            return JsonResponse({
                'success': False,
                'error': "An unknown error occurred when deleting image files."
            })


def navigate(request, method):
    photo = get_photo_from_request(request)

    try:
        nav = getattr(photo, method)(album=photo.album)
    except Photo.DoesNotExist:
        photos = Photo.objects.filter(album=photo.album)

        # At the oldest photo: return the newest
        if method == 'get_previous_by_taken':
            nav = photos.order_by('-taken')[0]

        # At the newest photo: return the oldest
        elif method == 'get_next_by_taken':
            nav = photos.order_by('taken')[0]

    return photo_to_response(nav)


@require_GET
def previous_photo(request):
    return navigate(request, 'get_previous_by_taken')


@require_GET
def next_photo(request):
    return navigate(request, 'get_next_by_taken')


def navigate_end(request, method):
    params = request.GET

    try:
        path = params.get('path')
    except KeyError:
        return JsonResponse({'error': "invalid parameters"}, status=400)

    album = get_album_by_path(path)
    photos = Photo.objects.filter(album=album).order_by('taken')

    if not photos:
        return JsonResponse({'error': "no photos in this album"}, status=404)

    photo = getattr(photos, method)()

    return photo_to_response(photo)


@require_GET
def first_photo(request):
    return navigate_end(request, 'first')


@require_GET
def last_photo(request):
    return navigate_end(request, 'last')


def search_photos(request):
    params = request.GET

    query = Q(album__hidden=False)

    name = params.get('name', '')
    if name:
        query = query & Q(album__name__icontains=name)

    location = params.get('location', '')
    if location:
        query = query & Q(album__location__icontains=location)

    width = params.get('width', '')
    if width:
        query = query & Q(width=int(width))

    height = params.get('height', '')
    if height:
        query = query & Q(height=int(height))

    rating = params.getlist('rating')
    if rating:
        subquery = Q()

        for value in rating:
            try:
                value = int(value)
            except ValueError:
                continue

            subquery = subquery | Q(rating=value)

        query = query & subquery

    order = params.get('order')

    if order not in ('taken', 'edited', 'uploaded'):
        order = 'taken'

    if params.get('direction') == 'new':
        order = f"-{order}"

    photos = Photo.objects.filter(query).order_by(order)

    count = photos.count()

    try:
        page = int(params.get('page'))
    except (ValueError, KeyError):
        page = 1

    start = ITEMS_PER_PAGE * (page - 1)
    end = start + ITEMS_PER_PAGE

    photos = photos[start:end]

    dicts = [generate_photo_dict(photo) for photo in photos]
    response = {
        'photos': dicts,
        'count': count,
    }

    return JsonResponse(response)
