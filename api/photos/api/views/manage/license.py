from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import LicenseSerializer
from photos.models import License


class ManageLicenseList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request) -> Response:
        licenses = License.objects.all()
        serializer = LicenseSerializer(licenses, many=True)

        return Response(serializer.data)
