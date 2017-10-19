from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET

from photos.models import Photo
from photos.views import get_album_by_path, get_exif

from pytz import timezone


def generate_response(photo):
    taken = photo.taken.astimezone(timezone(photo.album.timezone))

    return JsonResponse({
        'image_url': photo.image.url,
        'url': photo.get_absolute_url(),
        'metadata': {
            'taken': taken.strftime("%A, %Y-%m-%d, %-I:%M:%S %p"),
            'width': photo.width,
            'height': photo.height,
            'md5': photo.md5,
            'new_tab': photo.image.url,
            'download': reverse('download',
                                args=[photo.get_path(), photo.md5]),
        },
        'exif': get_exif(photo)
    })


def navigate(request, method):
    params = request.GET

    try:
        path = params.get('path')
        md5 = params.get('md5')
    except KeyError:
        return JsonResponse({'error': "invalid parameters"}, status=400)

    try:
        album = get_album_by_path(path)
        photo = Photo.objects.get(album=album, md5=md5)
    except Photo.DoesNotExist:
        return JsonResponse({'error': "photo does not exist"}, status=404)

    try:
        nav = getattr(photo, method)()
    except Photo.DoesNotExist:
        return JsonResponse({'error': "no more photos"}, status=404)

    return generate_response(nav)


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

    return generate_response(photo)


@require_GET
def first_photo(request):
    return navigate_end(request, 'first')


@require_GET
def last_photo(request):
    return navigate_end(request, 'last')
