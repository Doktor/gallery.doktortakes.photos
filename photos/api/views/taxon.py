from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Taxon, PhotoTaxon, Photo
from photos.api.serializers import TaxonSerializer, PhotoSerializer, SimplePhotoSerializer


class TaxonList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        taxa = Taxon.objects.all().prefetch_related('parent')
        serializer = TaxonSerializer(taxa, many=True)

        return Response(serializer.data)


class TaxonPhotoList(APIView):
    @staticmethod
    def get(request: Request, catalog_id: str) -> Response:
        if request.GET.get('recursive', False):
            objects = Taxon.objects.with_tree_fields()
            taxon = get_object_or_404(objects, catalog_id=catalog_id)
            taxa = taxon.descendants(include_self=True)

            links = PhotoTaxon.objects.filter(taxon__in=taxa)

            photo_ids = set(link.photo_id for link in links)
            photos = Photo.objects.filter(id__in=photo_ids) \
                .select_related('album') \
                .prefetch_related('thumbnails')
        else:
            taxon = get_object_or_404(Taxon, catalog_id=catalog_id)
            photos = taxon.photos.all()

        serializer = SimplePhotoSerializer(photos, many=True)
        return Response(serializer.data)
