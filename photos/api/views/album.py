from typing import List, Tuple

from django.http import Http404

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, SimpleAlbumSerializer, PhotoSerializer)
from photos.models import Album, Photo
from photos.utils.query import get_album_for_user_or_404, get_albums_for_user

from http import HTTPStatus as Status


class AlbumNotFound(exceptions.APIException):
    status_code = Status.NOT_FOUND

    def __init__(self):
        super().__init__("Album not found.")


def get_album(request: Request, path: str) -> Album:
    try:
        return get_album_for_user_or_404(request, path)
    except Http404:
        raise AlbumNotFound


def get_album_and_children(request: Request, path: str) -> Tuple[Album, List[Album]]:
    album = get_album(request, path)

    children = [
        c for c
        in album.children.select_related('cover').prefetch_related('cover__thumbnails')
        if c.check_access(request)
    ]

    return (album, children)


def get_photos_for_album(request: Request, path: str, recursive: bool = False) -> Response:
    album = get_album(request, path)

    if recursive:
        albums = album.get_all_subalbums(include_self=True)
        photos = Photo.objects.filter(album__in=albums)
    else:
        photos = album.photos

    photos = photos.order_by('taken').prefetch_related('album', 'thumbnails')

    serialized = []

    for index, photo in enumerate(photos):
        context = {
            'index': index,
            'is_staff': request.user.is_staff,
        }
        serialized.append(PhotoSerializer(photo, context=context).data)

    return Response({'photos': serialized}, status=Status.OK)


class AlbumList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        if request.GET.get('full', False):
            albums = get_albums_for_user(request.user, top_level_only=True) \
                .select_related('cover', 'parent') \
                .prefetch_related('children', 'tags', 'users', 'groups', 'cover__thumbnails')
            serializer_type = AlbumSerializer
        else:
            albums = get_albums_for_user(request.user, top_level_only=True) \
                .select_related('cover', 'parent') \
                .prefetch_related('cover__thumbnails')
            serializer_type = SimpleAlbumSerializer

        serializer = serializer_type(albums, many=True)
        return Response({'albums': serializer.data})


class AlbumDetail(APIView):
    @staticmethod
    def get(request: Request, path: str) -> Response:
        album, children = get_album_and_children(request, path)

        album_serializer = AlbumSerializer(album)
        children_serializer = SimpleAlbumSerializer(children, many=True)

        return Response({
            'album': album_serializer.data,
            'children': children_serializer.data,
        })


class AlbumPhotoList(APIView):
    @staticmethod
    def get(request: Request, path: str) -> Response:
        return get_photos_for_album(request, path, recursive=False)
