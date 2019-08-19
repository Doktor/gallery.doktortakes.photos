from django.core.cache import cache
from django.db.models import Q
from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.fields import (
    AlbumField, GroupField, PhotoHashField, TagField, UserField,
    get_album_by_path)
from photos.api.photo import PhotoSerializer
from photos.models.album import Album
from photos.models.photo import Photo
from photos.models.utils import generate_md5_hash, CHUNK_SIZE
from photos.utils import get_album_by_path

from http import HTTPStatus as Status
from io import BytesIO


class AlbumList(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        serializer = AlbumSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)


class AlbumDetail(APIView):
    def dispatch(self, request: Request, *args, **kwargs) -> Response:
        if not request.user.is_staff:
            raise ValidationError("Album does not exist.")

        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_album(path: str) -> Album:
        try:
            return get_album_by_path(path)
        except (Album.DoesNotExist, IndexError):
            raise Http404

    def get(self, request: Request, path: str) -> Response:
        album = self.get_album(path)
        serializer = AlbumSerializer(album)

        return Response(serializer.data)

    def patch(self, request: Request, path: str) -> Response:
        album = self.get_album(path)
        serializer = AlbumCoverSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    def put(self, request: Request, path: str) -> Response:
        album = self.get_album(path)
        serializer = AlbumSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    def delete(self, request: Request, path: str) -> Response:
        album = self.get_album(path)
        album.delete()

        return Response(status=Status.NO_CONTENT)


class AlbumSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True, source='get_path')

    tags = TagField(many=True, allow_empty=True, queryset=Q())
    users = UserField(many=True, allow_empty=True, queryset=Q())
    groups = GroupField(many=True, allow_empty=True, queryset=Q())
    parent = AlbumField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = (
            'name', 'slug', 'path',
            'place', 'location', 'description', 'tags',
            'start', 'end',
            'thumbnail_size',
            'access_level', 'password', 'users', 'groups',
            'parent',
        )


class AlbumCoverSerializer(serializers.ModelSerializer):
    cover = PhotoHashField(allow_empty=True, allow_null=True, queryset=Q())

    class Meta:
        model = Album
        fields = ('cover',)


class AlbumPhotoList(APIView):
    @staticmethod
    def get_album(path):
        return get_album_by_path(path)

    def get(self, request: Request, path: str) -> Response:
        album = self.get_album(path)

        if not album.check_access(request):
            return Response({'error': "Album does not exist."}, status=Status.NOT_FOUND)

        response = []
        photos = album.photos.filter(sidecar_exists=True).order_by('taken')

        for index, photo in enumerate(photos):
            context = {
                'index': index,
                'is_staff': request.user.is_staff,
            }
            response.append(PhotoSerializer(photo, context=context).data)

        return Response({'photos': response})

    def post(self, request: Request, path: str) -> Response:
        if not request.user.is_staff:
            return Response({'error': "Album does not exist."}, status=Status.NOT_FOUND)

        files = request.FILES.getlist('files')
        album = self.get_album(path)

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
