from datetime import datetime
import pytz

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from photos.api.serializers import AlbumForListViewSerializer
from photos.utils import get_albums_for_user


def get_formatted_time(dt: datetime) -> str:
    return dt.astimezone(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")


@api_view()
def get_current_user(request: Request) -> Response:
    user = request.user

    if user.is_superuser:
        status = "superuser"
    elif user.is_staff:
        status = "staff"
    elif user.is_authenticated:
        status = "user"
    else:
        return Response({"status": "anonymous"})

    return Response({
        "name": user.username,
        "status": status,
        "account_created": get_formatted_time(user.date_joined),
        "last_sign_in": get_formatted_time(user.last_login),
    })


@api_view()
def get_albums_for_current_user(request: Request) -> Response:
    albums = (get_albums_for_user(request.user, exclude_public=True)
              .select_related('cover')
              .prefetch_related('tags'))
    serializer = AlbumForListViewSerializer(albums, many=True)

    return Response({"albums": serializer.data})
