from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from photos.models import Photo
from photos.views import get_album_by_path

import functools
import json
from json import JSONDecodeError


class APIError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)

        self.message = message
        self.status = status

    def to_response(self):
        return JsonResponse({'error': self.message}, status=self.status)


def api_wrapper(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except APIError as e:
            return e.to_response()

    return wrapper


@method_decorator(api_wrapper, name='dispatch')
class APIView(View):
    def _get_data(self, request):
        content_type = request.META.get('CONTENT_TYPE', '')

        if not content_type.startswith('application/json'):
            raise APIError("Invalid content type.")

        try:
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            raise APIError("Invalid JSON data.")

        return data


def get_photo_from_request(request, path):
    params = request.GET

    try:
        md5 = params.get('md5')
    except KeyError:
        raise APIError("Missing parameters: 'md5' is required.")

    try:
        album = get_album_by_path(path)
        photo = Photo.objects.get(album=album, md5=md5)
    except Photo.DoesNotExist:
        raise APIError("Photo does not exist.", status=404)

    return photo
