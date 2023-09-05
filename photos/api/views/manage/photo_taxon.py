from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers.taxon import ManagePhotoTaxonSerializer
from photos.api.views.photo import get_photo

from http import HTTPStatus as Status

from photos.models import PhotoTaxon


class ManagePhotoTaxonList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        serializer = ManagePhotoTaxonSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=Status.BAD_REQUEST)

        serializer.save(photo=photo)
        return Response(serializer.data)


class ManagePhotoTaxonDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def put(request: Request, md5: str, catalog_id: str) -> Response:
        photo = get_photo(request, md5)
        link = PhotoTaxon.objects.get(photo=photo, taxon__catalog_id=catalog_id)
        serializer = ManagePhotoTaxonSerializer(link, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=Status.BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def delete(request: Request, md5: str, catalog_id: str) -> Response:
        photo = get_photo(request, md5)
        link = PhotoTaxon.objects.get(photo=photo, taxon__catalog_id=catalog_id)

        link.delete()

        return Response(status=Status.NO_CONTENT)