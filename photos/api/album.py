from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET

import json
from datetime import datetime
from json import JSONDecodeError

from core.context_processors import metadata
from photos.models import Photo

from .photo import generate_photo_dict
from .utils import APIError, get_album_from_request

m = metadata(None)


def generate_album_dict(album, method='GET'):
    if album.end:
        end = album.end.strftime("%Y-%m-%d")
    else:
        end = None

    response = {
        'url': album.get_absolute_url(),
        'path': album.get_path(),
        'name': album.name,
        'location': album.location,
        'description': album.description,
        'start': album.start.strftime("%Y-%m-%d"),
        'end': end,
    }

    if album.cover:
        response['cover'] = {
            'url': album.cover.image.url,
            'thumbnail_url': album.cover.thumbnail.url,
        }

    if method == 'PUT':
        response.update({
            'edit_url': album.get_edit_url(),
            'title': f"Editing {album.name} | {m.get('TITLE')}"
        })

    return response


class AlbumView(LoginRequiredMixin, View):
    required = (('name', 'album name'), ('start', 'start date'))

    def _get_data(self, request):
        content_type = request.META.get('CONTENT_TYPE', '')

        if not content_type.startswith('application/json'):
            raise APIError("Invalid content type.")

        try:
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            raise APIError("Invalid JSON data.")

        return data

    def get(self, request, *args, **kwargs):
        try:
            album = get_album_from_request(request)
        except APIError as e:
            return e.to_response()

        return JsonResponse(generate_album_dict(album))

    def patch(self, request, *args, **kwargs):
        try:
            data = self._get_data(request)
            album = get_album_from_request(request)
        except APIError as e:
            return e.to_response()

        md5 = data.get('md5')

        if not md5:
            return JsonResponse({})

        try:
            photo = Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            return JsonResponse({'error': "Photo does not exist."}, status=400)

        album.cover = photo
        album.save()

        response = generate_album_dict(album, method='PUT')
        response['message'] = "Album cover changed successfully."

        return JsonResponse(response)

    def put(self, request, *args, **kwargs):
        try:
            data = self._get_data(request)
            album = get_album_from_request(request)
        except APIError as e:
            return e.to_response()

        for key, name in self.required:
            if not data.get(key, ''):
                return JsonResponse(
                    {'error': f"The {name} can't be empty."}, status=400)

        for key in ('name', 'place', 'location', 'description'):
            setattr(album, key, data.get(key))

        for key in ('start', 'end'):
            if key == 'end' and not data.get(key, ''):
                album.end = None
                continue

            try:
                date = datetime.strptime(data.get(key), "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse(
                    {'error': "Invalid date format."}, status=400)

            setattr(album, key, date)

        try:
            album.clean()
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)

        album.save()

        response = generate_album_dict(album, method='PUT')
        response['message'] = "Album updated successfully."

        return JsonResponse(response)

    def delete(self, request, *args, **kwargs):
        try:
            album = get_album_from_request(request)
        except APIError as e:
            return e.to_response()

        if request.GET.get('name') != album.name:
            return JsonResponse({
                'success': False,
                'error': "Incorrect album name.",
            })

        album.delete()

        return JsonResponse({
            'success': True,
            'message': "Album deleted successfully. Redirecting...",
        })


@require_GET
def get_album_photos(request):
    album = get_album_from_request(request)
    photos = []

    if album.password and album.password != request.GET.get('password', ''):
        return JsonResponse({
            'success': False,
            'message': "Album does not exist."
        })

    for index, photo in enumerate(album.photos.all().order_by('taken')):
        photos.append(generate_photo_dict(photo, index))

    return JsonResponse({'photos': photos})
