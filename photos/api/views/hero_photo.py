from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from photos.api.serializers import HeroPhotoSerializer
from photos.models import HeroPhoto


@api_view()
def get_hero_photos(request: Request) -> Response:
    photos = HeroPhoto.objects.all()
    serializer = HeroPhotoSerializer(photos, many=True)

    return Response(serializer.data)
