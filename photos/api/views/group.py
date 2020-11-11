from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import GroupSerializer


class GroupList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request) -> Response:
        groups = Group.objects.all().prefetch_related('user_set')
        serializer = GroupSerializer(groups, many=True)

        return Response({'groups': serializer.data})
