from django.http import JsonResponse
from django.views.decorators.http import require_GET

from photos.models import Photo
from photos.views import get_album_by_path


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

    return JsonResponse({
        'md5': nav.md5,
        'image': nav.image.url,
        'url': nav.get_absolute_url()
    })


@require_GET
def previous_photo(request):
    return navigate(request, 'get_previous_by_taken')


@require_GET
def next_photo(request):
    return navigate(request, 'get_next_by_taken')
