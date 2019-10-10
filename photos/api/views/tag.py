from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import AlbumForListViewSerializer, TagSerializer
from photos.models import Tag
from photos.utils import get_albums_for_user, get_tags_for_user


class TagList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        tags = get_tags_for_user(request.user)
        serializer = TagSerializer(tags, many=True)

        return Response({"tags": serializer.data})


class TagDetail(APIView):
    @staticmethod
    def get(request: Request, slug: str) -> Response:
        try:
            tag = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            raise exceptions.NotFound

        albums = get_albums_for_user(request.user).filter(tags=tag).select_related('cover')

        album_serializer = AlbumForListViewSerializer(albums, many=True)
        tag_serializer = TagSerializer(tag)

        return Response({
            "albums": album_serializer.data,
            "tag": tag_serializer.data,
        })
