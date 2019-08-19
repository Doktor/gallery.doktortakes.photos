from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404

from photos.models import Album, Photo
from photos.utils.image import fit_image

from typing import List, Optional


def get_albums(path: str) -> List[Album]:
    """Returns all of the albums in the path. Raises Http404 if any part of the path is invalid."""
    path = path.split('/')

    if len(path) == 1:
        return [get_object_or_404(Album, slug=path[0], parent=None)]

    albums = []
    parent = None

    for item in path:
        album = get_object_or_404(Album, slug=item, parent=parent)
        albums.append(album)
        parent = album

    return albums


def get_album(path: str) -> Album:
    """Returns the last album in the path. Raises Http404 if the path is invalid."""
    return get_albums(path)[-1]


def get_photo(md5: str, request: HttpRequest, path: Optional[str] = None) -> Photo:
    if path is not None:
        album = get_album(path)
        photo = get_object_or_404(Photo, md5=md5, album=album)
    else:
        photo = get_object_or_404(Photo, md5=md5)

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    return photo
