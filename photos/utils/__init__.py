from django.shortcuts import get_object_or_404

from photos.models import Album

from typing import List

from photos.utils.image import thumbnail


def get_albums_from_path(path: str) -> List[Album]:
    """Returns a list of Albums extracted from the given path."""
    path = path.split('/')

    if len(path) == 1:
        return [get_object_or_404(Album, slug=path[0], parent=None)]

    albums = list()
    parent = None
    for item in path:
        album = get_object_or_404(Album, slug=item, parent=parent)
        albums.append(album)
        parent = album

    return albums


def get_album_by_path(path: str) -> Album:
    """Returns the Album corresponding to the given path."""
    return get_albums_from_path(path)[-1]
