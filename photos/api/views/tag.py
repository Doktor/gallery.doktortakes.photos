from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import TagSerializer
from photos.utils import get_tags_for_user


class TagList(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        tags = get_tags_for_user(request.user)
        serializer = TagSerializer(tags, many=True)

        return Response({"tags": serializer.data})
