from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from photos.api.serializers import AlbumForListViewSerializer
from photos.utils import get_albums_for_user


@api_view()
def get_current_user(request: Request) -> Response:
    if request.user.is_superuser:
        status = "superuser"
    elif request.user.is_staff:
        status = "staff"
    elif request.user.is_authenticated:
        status = "user"
    else:
        status = "anonymous"

    return Response({
        "name": request.user.username,
        "status": status,
    })


@api_view()
def get_albums_for_current_user(request: Request) -> Response:
    albums = (get_albums_for_user(request.user, exclude_public=True)
              .select_related('cover')
              .prefetch_related('tags'))
    serializer = AlbumForListViewSerializer(albums, many=True)

    return Response({"albums": serializer.data})
