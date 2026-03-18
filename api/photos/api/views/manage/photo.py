from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import PhotoSerializer, ManagePhotoUpdateSerializer
from photos.api.views.photo import get_photo, PhotoNotFound, PhotoDetail
from photos.models import Photo
from photos.utils import try_parse_int
from photos.utils.image import get_average_color

from http import HTTPStatus as Status
import PIL.Image


class ManagePhotoDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def patch(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        serializer = ManagePhotoUpdateSerializer(photo, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=Status.BAD_REQUEST)

        serializer.save()
        return PhotoDetail.get(request, md5)

    @staticmethod
    def delete(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        photo.delete()

        return Response(status=Status.NO_CONTENT)


class ManagePhotoAverageColor(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)

        if photo is None:
            return Response({}, status=Status.NOT_FOUND)

        image = PIL.Image.open(photo.original)
        photo.placeholder_color = get_average_color(image)
        photo.save()

        return Response({}, status=Status.OK)


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
