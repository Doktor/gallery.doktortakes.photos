from typing import Optional

from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import ThumbnailSerializer
from photos.models import Photo
from photos.api.views.photo import PhotoNotFound


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
