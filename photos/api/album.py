from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpRequest
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_GET

from datetime import datetime

from photos.api.utils import APIError, APIView, api_wrapper
from photos.models import Album, Photo, Tag
from photos.utils import get_album_by_path as get_album

User = get_user_model()


def get_album_by_path(path: str):
    try:
        return get_album(path)
    except Album.DoesNotExist:
        raise APIError("The specified album doesn't exist.")


class AlbumView(APIView):
    """Handles all CRUD operations for Album objects.
    Access is restricted to staff users."""

    required = (('name', 'album name'), ('start', 'start date'))

    def _apply_changes(self, request: HttpRequest, album: Album) -> Album:
        data = self._get_data(request)

        # General

        for key, f_name in self.required:
            if not data.get(key, ''):
                raise APIError(f"Field '{f_name}' can't be empty.")

        for key in ('name', 'place', 'location', 'description', 'password'):
            setattr(album, key, data.get(key))

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

        # Access permissions

        level = data.get('level', '')

        if level:
            album.access_level = level

        users_string = data.get('users', '')

        if users_string:
            new_users, new_groups = [], []

            for name in users_string.split(', '):
                name = name.strip()

                try:
                    user = User.objects.get(username__iexact=name)
                except User.DoesNotExist:
                    raise APIError(f"The user '{name}' does not exist.")
                else:
                    new_users.append(user)

            album.users.clear()
            album.users.add(*new_users)

        groups_string = data.get('groups', '')

        if groups_string:
            new_groups = []

            for name in groups_string.split(', '):
                name = name.strip()

                if name.lower().startswith('group:'):
                    try:
                        name = name[6:].strip()
                        group = Group.objects.get(name__iexact=name)
                    except Group.DoesNotExist:
                        raise APIError(f"The group '{name}' does not exist.")
                    else:
                        new_groups.append(group)
                else:
                    continue

            album.groups.clear()
            album.groups.add(*new_groups)

        # Tags

        if album.pk:
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

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpRequest:
        if not request.user.is_staff:
            raise APIError("Album does not exist.")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, path: str) -> JsonResponse:
        album = get_album_by_path(path)
        return JsonResponse(album.serialize(edit=True))

    def post(self, request: HttpRequest) -> JsonResponse:
        album = self._apply_changes(request, Album())
        album.save()

        return JsonResponse({
            'message': "Album created successfully. Redirecting...",
            'redirect': album.get_edit_url(),
        })

    def put(self, request: HttpRequest, path: str) -> JsonResponse:
        album = get_album_by_path(path)
        album = self._apply_changes(request, album)
        album.save()

        return JsonResponse({
            'message': "Album updated successfully.",
            'title': f"Editing {album.name} | Doktor Takes Photos",
            'edit_url': reverse('edit_album', kwargs={'path': album.get_path()}),
            'album': album.serialize(edit=True),
        })

    def patch(self, request: HttpRequest, path: str) -> JsonResponse:
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

    def delete(self, request: HttpRequest, path: str) -> JsonResponse:
        album = get_album_by_path(path)

        if request.GET.get('name') != album.name:
            raise APIError("Incorrect album name.")

        album.delete()

        return JsonResponse({
            'message': "Album deleted successfully. Redirecting...",
        })


@api_wrapper
@require_GET
def get_album_photos(request: HttpRequest, path: str) -> JsonResponse:
    album: Album = get_album_by_path(path)
    response = []

    if not album.check_access(request):
        raise APIError("Album does not exist.")

    photos = album.photos.filter(sidecar_exists=True).order_by('taken')
    admin = request.user.is_staff

    for index, photo in enumerate(photos):
        response.append(photo.serialize(admin=admin, index=index))

    return JsonResponse({'photos': response})
