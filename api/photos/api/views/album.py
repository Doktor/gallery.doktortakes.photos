from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import Http404

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, SimpleAlbumSerializer, PhotoSerializer)
from photos.models.album import AlbumType, ACCESS_LEVELS, Allow
from photos.models import Album, Photo, Tag
from photos.utils.query import get_album_for_user_or_404, get_albums_for_user

from http import HTTPStatus as Status

User = get_user_model()


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
        in (album.children.
            select_related('cover').
            prefetch_related('cover__thumbnails').
            order_by('start', 'name'))
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

    photos = photos.order_by('taken').prefetch_related('album', 'thumbnails', 'taxa', 'taxa__taxon')

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
        if user_id := request.GET.get('user_id', False):
            user = User.objects.get(id=user_id)

            if request.user.id != user and not request.user.is_staff:
                return Response({}, status=Status.FORBIDDEN)

            target_user = user
        else:
            target_user = request.user

        albums = (
            get_albums_for_user(target_user, top_level_only=True).
            select_related('cover', 'parent')
        )

        if user_id:
            albums = albums.filter(access_level__gt=Allow.PUBLIC)

        if (tag_slug := request.GET.get('tag', None)) is not None:
            tag = Tag.objects.get(slug=tag_slug)
            albums = albums.filter(tags=tag)

        albums = albums.prefetch_related('cover__thumbnails')
        serializer = SimpleAlbumSerializer(albums, many=True)

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


class FeaturedAlbumList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        albums = Album.objects.filter(type=AlbumType.FEATURED) \
            .annotate(size=Count('photos')) \
            .select_related('cover', 'parent') \
            .prefetch_related('cover__thumbnails')
        serializer = SimpleAlbumSerializer(albums, many=True)
        return Response({'albums': serializer.data})
