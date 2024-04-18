from django.core.files import File
from django.db import transaction

from rest_framework import exceptions
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import (
    AlbumSerializer, AlbumCoverSerializer, PhotoSerializer)
from photos.api.views.album import get_album, get_photos_for_album
from photos.models import Photo
from photos.tasks import create_thumbnails
from photos.utils.metadata import parse_exif_data, parse_xmp_data
from photos.utils.models import format_file_size, generate_md5_hash, CHUNK_SIZE

from http import HTTPStatus as Status
from io import BytesIO
import PIL.Image


class ManageAlbumList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request) -> Response:
        serializer = AlbumSerializer(data=request.data)

        if serializer.is_valid():
            album = serializer.save()
            return Response(serializer.data, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)


class ManageAlbumDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def patch(request: Request, path: str) -> Response:
        album = get_album(request, path)
        serializer = AlbumCoverSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()

            photo = PhotoSerializer(album.cover)
            return Response(photo.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    @staticmethod
    def put(request: Request, path: str) -> Response:
        album = get_album(request, path)
        serializer = AlbumSerializer(album, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=Status.BAD_REQUEST)

    @staticmethod
    def delete(request: Request, path: str) -> Response:
        album = get_album(request, path)
        album.delete()

        return Response(None, status=Status.NO_CONTENT)


class ManageAlbumPhotoList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request, path: str) -> Response:
        return get_photos_for_album(request, path, recursive='recursive' in request.GET)

    @staticmethod
    def post(request: Request, path: str) -> Response:
        file = request.FILES.get('file')

        # Check if this image already exists
        md5 = generate_md5_hash(file)

        if Photo.objects.filter(md5=md5).exists():
            raise exceptions.ValidationError(f"Duplicate file: {md5}")

        album = get_album(request, path)

        # Make a copy of the file to generate thumbnails later
        copy = BytesIO()
        copy.name = file.name

        for chunk in file.chunks(chunk_size=CHUNK_SIZE):
            copy.write(chunk)

        # Parse metadata
        photo = Photo()
        photo.album = album
        photo.md5 = md5
        photo.original_filename = file.name

        parse_exif_data(photo, file)
        parse_xmp_data(photo, file)

        file.seek(0)
        image = PIL.Image.open(file)
        photo.width = image.width
        photo.height = image.height

        photo.file_size = format_file_size(file.size)

        # Save
        file.seek(0)
        photo.original.save(file.name, File(file), save=False)

        with transaction.atomic():
            # If an existing photo has the same file name, replace it
            try:
                original = Photo.objects.get(album=album, original_filename=file.name)
            except Photo.DoesNotExist:
                pass
            else:
                original.delete()

            photo.save()

            # It looks like the storage backend closes the file after saving it,
            # so we need to operate on a copy of the file here: the file can't be
            # reopened because it's an in-memory file.
            create_thumbnails(photo, File(copy))

        serializer = PhotoSerializer(photo)
        return Response(serializer.data, status=Status.OK)

    @staticmethod
    def delete(request: Request, path: str) -> Response:
        album = get_album(request, path)

        try:
            hashes = request.data['photos']
        except KeyError:
            raise exceptions.ValidationError("No photos were specified.")

        for photo in album.photos.filter(md5__in=hashes):
            photo.delete()

        return Response(status=Status.NO_CONTENT)
