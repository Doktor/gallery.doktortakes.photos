from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404

from photos.models import Album, Photo
from photos.utils.image import fit_image

from typing import List, Optional


def get_albums(path: str) -> List[Album]:
    base = get_object_or_404(Album, path=path)
    albums = [base]

    while base.parent is not None:
        albums.append(base.parent)
        base = base.parent

    return albums[::-1]


def get_album(path: str) -> Album:
    return get_object_or_404(Album, path=path)


def get_photo(md5: str, request: HttpRequest,
              path: Optional[str] = None, select_album: bool = False) -> Photo:
    qs = Photo.objects.filter(md5=md5)

    if path is not None:
        qs = qs.filter(album__path=path)

    if select_album:
        qs = qs.select_related('album')

    if not qs:
        raise Http404

    photo = qs[0]

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    return photo
