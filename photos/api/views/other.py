from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from photos.api.serializers import AlbumForListViewSerializer
from photos.models import Album
from photos.settings import GIT_STATUS


@api_view()
def get_recent(request: Request) -> Response:
    recent_albums = (
        Album.objects.order_by('-start')
            .annotate(last_upload=Max('photos__uploaded'))
            .filter(last_upload__isnull=False)
            .order_by('-last_upload')
            .select_related('cover')
            .prefetch_related('tags')
    )[:30]

    return Response({
        "recent_albums": AlbumForListViewSerializer(recent_albums, many=True).data,
        "git_status": GIT_STATUS,
    })
