from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import UserSerializer

User = get_user_model()


class UserList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request) -> Response:
        users = User.objects.all().prefetch_related('groups')
        serializer = UserSerializer(users, many=True)

        return Response({'users': serializer.data})
