from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import SimpleAlbumSerializer
from photos.models.album import Album, AlbumType


class ExternalAlbumList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        albums = Album.objects.filter(type=AlbumType.EXTERNAL)
        serializer = SimpleAlbumSerializer(albums, many=True)

        return Response({'albums': serializer.data})
