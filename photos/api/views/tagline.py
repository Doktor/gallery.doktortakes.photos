from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from photos.models import Tagline

from random import randint


@api_view()
def get_tagline(request: Request) -> Response:
    count = Tagline.objects.count()
    tagline = Tagline.objects.all()[randint(0, count - 1)]

    return Response(tagline.text)
