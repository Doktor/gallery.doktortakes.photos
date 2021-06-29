from django.db.models import QuerySet, Q
from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from photos.models import Album, Photo, Tag
from photos.models.album import Allow

from typing import List, Optional, Union


def get_albums(path: str) -> List[Album]:
    base = get_object_or_404(Album, path=path)
    albums = [base]

    while base.parent is not None:
        albums.append(base.parent)
        base = base.parent

    return albums[::-1]


def get_album(path: str) -> Optional[Album]:
    try:
        return Album.objects.get(path=path)
    except Album.DoesNotExist:
        return None


def get_album_for_user_or_404(request: Union[HttpRequest, Request], path: str) -> Album:
    album = get_object_or_404(Album, path=path)

    if album.check_access(request):
        return album

    raise Http404


def get_photo_for_user_or_404(request: Union[HttpRequest, Request], md5: str,
                              path: Optional[str] = None, select_album: bool = False) -> Photo:
    qs = Photo.objects.filter(md5=md5)

    if path is not None:
        qs = qs.filter(album__path=path)

    if select_album:
        qs = qs.select_related('album')

    if not qs:
        raise Http404

    photo = qs.first()

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    return photo


def get_albums_for_user(user, exclude_public=False, include_children=False) -> QuerySet:
    """Returns a QuerySet of the albums that a user has access to."""
    q = Q() if include_children else Q(parent__isnull=True)

    if user.is_superuser:
        q &= Q(access_level__lte=Allow.SUPERUSER)
    elif user.is_staff:
        q &= Q(access_level__lte=Allow.STAFF)
    elif user.is_authenticated:
        # Direct ownership
        owner_q = Q(users=user)

        # Group (indirect) ownership
        for group in user.groups.all():
            owner_q |= Q(groups=group)

        owner_q &= Q(access_level__lte=Allow.OWNERS)

        # Everything else
        q = owner_q | Q(access_level__lte=Allow.SIGNED_IN)
    elif user.is_anonymous:
        q &= Q(access_level=Allow.PUBLIC)

    if exclude_public:
        q &= Q(access_level__gt=Allow.PUBLIC)

    return Album.objects.filter(q).distinct().order_by('-start')


def get_tags_for_user(user) -> QuerySet:
    """Returns a QuerySet of the tags on the albums that a user has access to."""
    return (
        Tag.objects
            .filter(albums__in=get_albums_for_user(user))
            .distinct()
            .order_by('slug'))
