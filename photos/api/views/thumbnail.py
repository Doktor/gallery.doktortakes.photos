from http import HTTPStatus as Status
from typing import Optional

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import ThumbnailSerializer
from photos.api.views.photo import PhotoNotFound
from photos.api.views.validation import validate_multiple, validate_is_positive_number, validate_is_not_none
from photos.models import Photo
from photos.utils.image import create_thumbnail


def get_photo(request, md5) -> Optional[Photo]:
    if not request.user.is_staff:
        raise exceptions.PermissionDenied("Not authorized.")

    try:
        return Photo.objects.get(md5=md5)
    except Photo.DoesNotExist:
        return None


class ThumbnailList(APIView):
    @staticmethod
    def get(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)

        if photo is None:
            raise PhotoNotFound

        thumbnails = photo.thumbnails.all()
        serializer = ThumbnailSerializer(thumbnails, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)

        if photo is None:
            raise PhotoNotFound

        validators = [
            validate_is_not_none,
            validate_is_positive_number,
        ]

        width = request.data.get('width', None)
        width_errors = validate_multiple('width', width, validators)

        height = request.data.get('height', None)
        height_errors = validate_multiple('height', height, validators)

        errors = width_errors + height_errors
        if errors:
            return Response({'error': errors}, status=Status.BAD_REQUEST)

        name = request.data.get("name", '')
        add_watermark = request.data.get("addWatermark", False)
        watermark_color = request.data.get("watermarkColor", None)

        thumbnail = create_thumbnail(
            photo.pk, None,
            width, height, name,
            add_watermark=add_watermark, watermark_color=watermark_color)
        serializer = ThumbnailSerializer(thumbnail)
        return Response(serializer.data)
