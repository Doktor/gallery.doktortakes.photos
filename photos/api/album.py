from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET

from .photo import generate_photo_dict
from .utils import APIError, get_album_from_request


class AlbumView(LoginRequiredMixin, View):
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

    for index, photo in enumerate(album.photos.all().order_by('taken')):
        photos.append(generate_photo_dict(photo, index))

    return JsonResponse({'photos': photos})
