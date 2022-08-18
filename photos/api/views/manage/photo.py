from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.views.photo import get_photo

from http import HTTPStatus as Status


class ManagePhotoDetail(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def delete(request: Request, md5: str) -> Response:
        photo = get_photo(request, md5)
        photo.delete()

        return Response(status=Status.NO_CONTENT)
