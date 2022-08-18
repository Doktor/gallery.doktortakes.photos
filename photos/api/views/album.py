from django.http import Http404

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, SimpleAlbumSerializer, PhotoSerializer)
from photos.models import Album
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
        album = get_album(request, path)
        serializer = AlbumSerializer(album)

        return Response(serializer.data)


class AlbumPhotoList(APIView):
    @staticmethod
    def get(request: Request, path: str) -> Response:
        album = get_album(request, path)

        response = []
        photos = album.photos.filter(sidecar_exists=True).order_by('taken').prefetch_related('thumbnails')

        for index, photo in enumerate(photos):
            context = {
                'index': index,
                'is_staff': request.user.is_staff,
            }
            response.append(PhotoSerializer(photo, context=context).data)

        return Response({'photos': response}, status=Status.OK)
