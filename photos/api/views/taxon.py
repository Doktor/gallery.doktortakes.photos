from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Taxon
from photos.api.serializers import TaxonSerializer


class TaxonList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        taxa = Taxon.objects.all().prefetch_related('parent')
        serializer = TaxonSerializer(taxa, many=True)

        return Response(serializer.data)
