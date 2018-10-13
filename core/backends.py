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

        # Staff users have access to everything
        if user.is_staff:
            return True

        album = obj

        # Auth backends can't handle passwords, defer to Album.check_access
        if album.password:
            return False

        # Access list does not exist
        if not album.users.exists() and not album.groups.exists():
            return True
        # Access list exists, but we're checking an anonymous user
        elif not user.is_authenticated:
            return False

        if user in album.users.all():
            return True

        if any(group in user.groups.all() for group in album.groups.all()):
            return True

        return False
