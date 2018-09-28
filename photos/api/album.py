from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.http import require_GET

from datetime import datetime

from photos.api.utils import APIError, APIView, api_wrapper
from photos.models import Album, Photo, Tag
from photos.views import get_album_by_path as get_album


def get_album_by_path(path):
    try:
        return get_album(path)
    except Album.DoesNotExist:
        raise APIError("The specified album doesn't exist.")


class AlbumView(LoginRequiredMixin, APIView):
    # Required fields: internal name, display name
    required = (('name', 'album name'), ('start', 'start date'))

    def _apply_changes(self, request, album):
        data = self._get_data(request)

        # General

        for key, f_name in self.required:
            if not data.get(key, ''):
                raise APIError(f"Field '{f_name}' can't be empty.")

        for key in ('name', 'place', 'location', 'description', 'password'):
            setattr(album, key, data.get(key))

        album.hidden = bool(int(data.get('hidden', 0)))

        # Dates

        for key in ('start', 'end'):
            if key == 'end' and not data.get(key, ''):
                album.end = None
                continue

            try:
                date = datetime.strptime(data.get(key), "%Y-%m-%d").date()
            except ValueError:
                raise APIError("Invalid date format.")

            setattr(album, key, date)

        if album.pk:
            # Tags

            album.tags.clear()
            tags = data.get('tags', '')

            if tags:
                for slug in tags.split(','):
                    slug = slugify(slug.strip().lower())

                    if not slug:
                        continue

                    try:
                        tag = Tag.objects.get(slug=slug)
                    except Tag.DoesNotExist:
                        tag = Tag.objects.create(slug=slug)

                    album.tags.add(tag)

        # Parent album

        parent_path = data.get('parent', '')

        if not parent_path:
            album.parent = None
        else:
            parent = get_album_by_path(parent_path)
            if parent == album:
                raise APIError("An album can't be its own parent.")
            album.parent = parent

        # Clean

        try:
            album.clean()
        except ValidationError as e:
            raise APIError(e.message)

        return album

    def get(self, request, path):
        album = get_album_by_path(path)
        return JsonResponse(album.serialize())

    def post(self, request):
        album = self._apply_changes(request, Album())
        album.save()

        return JsonResponse({
            'message': "Album created successfully. Redirecting...",
            'redirect': album.get_edit_url(),
        })

    def put(self, request, path):
        album = get_album_by_path(path)
        album = self._apply_changes(request, album)
        album.save()

        return JsonResponse({
            'message': "Album updated successfully.",
            'album': album.serialize(method='PUT'),
        })

    def patch(self, request, path):
        album = get_album_by_path(path)
        md5 = self._get_data(request).get('md5', '')

        try:
            photo = Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            raise APIError("Photo does not exist.")

        album.cover = photo
        album.save()

        return JsonResponse({
            'message': "Album cover changed successfully.",
            'album': album.serialize(),
        })

    def delete(self, request, path):
        album = get_album_by_path(path)

        if request.GET.get('name') != album.name:
            raise APIError("Incorrect album name.")

        album.delete()

        return JsonResponse({
            'message': "Album deleted successfully. Redirecting...",
        })


@api_wrapper
@require_GET
def get_album_photos(request, path):
    album = get_album_by_path(path)
    photos = []

    if album.password and album.password != request.GET.get('password', ''):
        raise APIError("Album does not exist.")

    for index, photo in enumerate(album.photos.all().order_by('taken')):
        photos.append(photo.serialize(index=index, filmstrip=False))

    return JsonResponse({'photos': photos})
