from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Taxon
from photos.api.serializers import TaxonSerializer, PhotoSerializer


class TaxonList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        taxa = Taxon.objects.all().prefetch_related('parent')
        serializer = TaxonSerializer(taxa, many=True)

        return Response(serializer.data)


class TaxonPhotoList(APIView):
    @staticmethod
    def get(request: Request, catalog_id: str) -> Response:
        taxon = get_object_or_404(Taxon, catalog_id=catalog_id)
        photos = taxon.photos.all()
        serializer = PhotoSerializer(photos, many=True)

        return Response(serializer.data)
