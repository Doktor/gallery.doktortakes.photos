from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import TaxonSerializer

from http import HTTPStatus as Status


class ManageTaxonList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(request: Request) -> Response:
        serializer = TaxonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=Status.CREATED)

        return Response(serializer.errors, status=Status.BAD_REQUEST)
