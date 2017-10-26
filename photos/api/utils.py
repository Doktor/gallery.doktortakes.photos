from django.http import JsonResponse

from photos.models import Album, Photo
from photos.views import get_album_by_path


class APIError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)

        self.message = message
        self.status = status

    def to_response(self):
        return JsonResponse({'error': self.message}, status=self.status)


def get_photo_from_request(request):
    params = request.GET

    try:
        path = params.get('path')
        md5 = params.get('md5')
    except KeyError:
        raise APIError("Missing parameters: 'path' and 'md5' are required.")

    try:
        album = get_album_by_path(path)
        photo = Photo.objects.get(album=album, md5=md5)
    except Photo.DoesNotExist:
        raise APIError("Photo does not exist.", status=404)

    return photo


def get_album_from_request(request):
    params = request.GET

    try:
        path = params.get('path')
    except KeyError:
        raise APIError("Missing parameters: 'path' is required.")

    try:
        album = get_album_by_path(path)
    except Album.DoesNotExist:
        raise APIError("Album does not exist.", status=404)

    return album
