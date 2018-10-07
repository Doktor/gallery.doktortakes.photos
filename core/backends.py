from django.core.exceptions import PermissionDenied

from photos.models import Album


class AlbumPermissionsBackend:
    def authenticate(self, request, **credentials):
        raise NotImplementedError

    def get_user(self, user_id):
        raise NotImplementedError

    def has_perm(self, user, permission, obj=None):
        if obj is None:
            return False

        if not isinstance(obj, Album):
            return False

        if permission != 'view':
            return False

        if user.is_staff:
            return True

        album = obj

        if album.password:
            return False

        if not album.users.exists() and not album.groups.exists():
            return True

        if user in album.users.all():
            return True

        if any(group in user.groups.all() for group in album.groups.all()):
            return True

        raise PermissionDenied
