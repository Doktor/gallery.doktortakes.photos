from django.core.cache import cache
from django.http import Http404

from rest_framework import exceptions, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, AlbumCoverSerializer, PhotoSerializer)
from photos.models import Album, Photo
from photos.models.utils import generate_md5_hash, CHUNK_SIZE
from photos.utils import get_album, get_albums_for_user

from http import HTTPStatus as Status
from io import BytesIO


class AlbumList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        albums = (get_albums_for_user(request.user, include_children=True)
                  .select_related('cover', 'parent')
                  .prefetch_related('children', 'tags', 'users', 'groups'))
        serializer = AlbumSerializer(albums, many=True)

        return Response({'albums': serializer.data})

    @staticmethod
    def post(request: Request) -> Response:
        if not request.user.is_staff:
            raise exceptions.PermissionDenied

        serializer = AlbumSerializer(data=request.data)

        if serializer.is_valid():
            album = serializer.save()
            response = {'path': album.path}

            return Response(response, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)


class AlbumDetail(APIView):
    @staticmethod
    def get_album(request: Request, path: str) -> Album:
        try:
            album = get_album(path)
        except Http404:
            raise exceptions.NotFound

        if not album.check_access(request):
            raise exceptions.NotFound

        if request.method not in permissions.SAFE_METHODS and not request.user.is_staff:
            raise exceptions.PermissionDenied

        return album

    # Methods

    def get(self, request: Request, path: str) -> Response:
        album = self.get_album(request, path)
        serializer = AlbumSerializer(album)

        return Response(serializer.data)

    def patch(self, request: Request, path: str) -> Response:
        album = self.get_album(request, path)
        serializer = AlbumCoverSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()

            photo = PhotoSerializer(album.cover)
            return Response(photo.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    def put(self, request: Request, path: str) -> Response:
        album = self.get_album(request, path)
        serializer = AlbumSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    def delete(self, request: Request, path: str) -> Response:
        album = self.get_album(request, path)
        album.delete()

        return Response(None, status=Status.NO_CONTENT)


class AlbumPhotoList(APIView):
    @staticmethod
    def get(request: Request, path: str) -> Response:
        album = get_album(path)

        if not album.check_access(request):
            raise ValidationError("Album does not exist.", code=Status.NOT_FOUND)

        response = []
        photos = album.photos.filter(sidecar_exists=True).order_by('taken')

        for index, photo in enumerate(photos):
            context = {
                'index': index,
                'is_staff': request.user.is_staff,
            }
            response.append(PhotoSerializer(photo, context=context).data)

        return Response({'photos': response}, status=Status.OK)

    @staticmethod
    def post(request: Request, path: str) -> Response:
        if not request.user.is_staff:
            raise ValidationError("Album does not exist.", code=Status.NOT_FOUND)

        files = request.FILES.getlist('files')
        album = get_album(path)

        photos = []

        for file in files:
            photo = Photo()
            photo.album = album

            # Check if this image already exists
            md5 = generate_md5_hash(file)

            try:
                Photo.objects.get(md5=md5)
            except Photo.DoesNotExist:
                pass
            else:
                raise ValidationError(f"Duplicate file: {md5}")

            photo.md5 = md5

            filename = file.name

            try:
                original = Photo.objects.get(album=album,
                                             original_filename=filename)
            except Photo.DoesNotExist:
                pass
            else:
                original.delete()

            data = BytesIO()
            data.name = filename

            photo.original_filename = filename

            for chunk in file.chunks(chunk_size=CHUNK_SIZE):
                data.write(chunk)

            # Expires after 24 hours
            cache.set(md5, data, 60 * 60 * 24)

            photo.save()
            photos.append(PhotoSerializer(photo).data)

        return Response({'photos': photos}, status=Status.OK)

    @staticmethod
    def delete(request: Request, path: str) -> Response:
        if not request.user.is_staff:
            raise ValidationError("Not authorized.", code=Status.UNAUTHORIZED)

        album = get_album(path)

        try:
            hashes = request.data['photos']
        except KeyError:
            raise ValidationError("No photos were specified.", code=Status.BAD_REQUEST)

        for photo in Photo.objects.filter(album=album, md5__in=hashes):
            photo.delete()

        return Response(status=Status.NO_CONTENT)
