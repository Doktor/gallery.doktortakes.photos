from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import ManagePhotoTaxonSerializer, TaxonSerializer
from photos.api.views.photo import get_photo

from http import HTTPStatus as Status

from photos.models import PhotoTaxon


class ManagePhotoTaxonList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        link_serializer = ManagePhotoTaxonSerializer(data=request.data)

        if not link_serializer.is_valid():
            return Response(link_serializer.errors, status=Status.BAD_REQUEST)

        link = link_serializer.save(photo=photo)
        taxon = TaxonSerializer(link.taxon)

        return Response({**link_serializer.data, **taxon.data})


class ManagePhotoTaxonDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def put(request: Request, md5: str, catalog_id: str) -> Response:
        photo = get_photo(request, md5)
        link = PhotoTaxon.objects.get(photo=photo, taxon__catalog_id=catalog_id)
        link_serializer = ManagePhotoTaxonSerializer(link, data=request.data)

        if not link_serializer.is_valid():
            return Response(link_serializer.errors, status=Status.BAD_REQUEST)

        link = link_serializer.save(photo=photo)
        taxon = TaxonSerializer(link.taxon)

        return Response({**link_serializer.data, **taxon.data})

    @staticmethod
    def delete(request: Request, md5: str, catalog_id: str) -> Response:
        photo = get_photo(request, md5)
        link = PhotoTaxon.objects.get(photo=photo, taxon__catalog_id=catalog_id)

        link.delete()
        return Response(status=Status.NO_CONTENT)
