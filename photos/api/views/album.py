from django.core.cache import cache
from django.core.files import File
from django.http import Http404

from rest_framework import exceptions, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, AlbumCoverSerializer, SimpleAlbumSerializer, PhotoSerializer)
from photos.models import Album, Photo
from photos.utils.image import check_dimensions
from photos.utils.metadata import parse_exif_data, parse_xmp_data
from photos.utils.models import generate_md5_hash, CHUNK_SIZE
from photos.utils.query import get_album_for_user_or_404, get_albums_for_user

from http import HTTPStatus as Status
from io import BytesIO
import PIL.Image


class AlbumNotFound(exceptions.APIException):
    status_code = Status.NOT_FOUND

    def __init__(self):
        super().__init__("Album not found.")


class AlbumList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        if request.GET.get('full', False):
            albums = get_albums_for_user(request.user, top_level_only=True) \
                .select_related('cover', 'parent') \
                .prefetch_related('children', 'tags', 'users', 'groups')
            serializer_type = AlbumSerializer
        else:
            albums = get_albums_for_user(request.user, top_level_only=True) \
                .select_related('cover', 'parent')
            serializer_type = SimpleAlbumSerializer

        serializer = serializer_type(albums, many=True)
        return Response({'albums': serializer.data})

    @staticmethod
    def post(request: Request) -> Response:
        if not request.user.is_staff:
            raise exceptions.PermissionDenied("Not authorized.")

        serializer = AlbumSerializer(data=request.data)

        if serializer.is_valid():
            album = serializer.save()
            return Response(serializer.data, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)


class AlbumDetail(APIView):
    @staticmethod
    def get_album(request: Request, path: str) -> Album:
        try:
            album = get_album_for_user_or_404(request, path)
        except Http404:
            raise AlbumNotFound

        if request.method not in permissions.SAFE_METHODS and not request.user.is_staff:
            raise exceptions.PermissionDenied("Not authorized.")

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
    def get_album(request: Request, path: str) -> Album:
        try:
            return get_album_for_user_or_404(request, path)
        except Http404:
            raise AlbumNotFound

    def get(self, request: Request, path: str) -> Response:
        album = self.get_album(request, path)

        response = []
        photos = album.photos.filter(sidecar_exists=True).order_by('taken').prefetch_related('thumbnails')

        for index, photo in enumerate(photos):
            context = {
                'index': index,
                'is_staff': request.user.is_staff,
            }
            response.append(PhotoSerializer(photo, context=context).data)

        return Response({'photos': response}, status=Status.OK)

    def post(self, request: Request, path: str) -> Response:
        if not request.user.is_staff:
            raise AlbumNotFound

        file = request.FILES.get('file')
        album = self.get_album(request, path)

        photo = Photo()
        photo.album = album

        # Check if this image already exists
        md5 = generate_md5_hash(file)

        try:
            Photo.objects.get(md5=md5)
        except Photo.DoesNotExist:
            pass
        else:
            raise exceptions.ValidationError(f"Duplicate file: {md5}")

        photo.md5 = md5

        filename = file.name

        try:
            original = Photo.objects.get(album=album, original_filename=filename)
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

        file.seek(0)
        check_dimensions(file)
        parse_exif_data(photo, file)
        parse_xmp_data(photo, file)

        file.seek(0)
        image = PIL.Image.open(file)
        photo.width = image.width
        photo.height = image.height

        file.seek(0)
        photo.original.save(file.name, File(file), save=False)

        photo.save()

        serializer = PhotoSerializer(photo)
        return Response(serializer.data, status=Status.OK)

    def delete(self, request: Request, path: str) -> Response:
        if not request.user.is_staff:
            raise exceptions.PermissionDenied("Not authorized.")

        album = self.get_album(request, path)

        try:
            hashes = request.data['photos']
        except KeyError:
            raise exceptions.ValidationError("No photos were specified.")

        for photo in album.photos.filter(md5__in=hashes):
            photo.delete()

        return Response(status=Status.NO_CONTENT)
