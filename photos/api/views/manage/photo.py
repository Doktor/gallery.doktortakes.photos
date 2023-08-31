from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import PhotoSerializer
from photos.api.views.photo import get_photo
from photos.models import Photo

from http import HTTPStatus as Status


class ManagePhotoDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def delete(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        photo.delete()

        return Response(status=Status.NO_CONTENT)


class ManageRecentPhotoList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request) -> Response:
        limit = request.data.get('limit', 12)

        photos = Photo.objects.all().order_by('-uploaded')[0:limit]
        serializer = PhotoSerializer(photos, many=True)

        return Response(serializer.data, status=Status.OK)
