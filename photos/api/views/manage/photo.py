from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import PhotoSerializer
from photos.api.views.photo import get_photo
from photos.models import Photo

from http import HTTPStatus as Status

from photos.utils import try_parse_int


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
        page = try_parse_int(request.GET.get('page', 1), 1)
        size = try_parse_int(request.GET.get('size', 12), 12)

        start = (page - 1) * size
        end = page * size

        photos = Photo.objects.all().order_by('-uploaded')[start:end]
        count = Photo.objects.count()

        serializer = PhotoSerializer(photos, many=True)

        return Response({"items": serializer.data, "count": count}, status=Status.OK)
