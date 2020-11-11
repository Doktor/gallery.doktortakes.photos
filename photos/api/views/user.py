from datetime import datetime
from http import HTTPStatus
import pytz

from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.api.serializers import UserSerializer

User = get_user_model()


def get_formatted_time(dt: datetime) -> str:
    return dt.astimezone(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")


class UserList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request: Request) -> Response:
        users = User.objects.all().prefetch_related('groups')
        serializer = UserSerializer(users, many=True)

        return Response({'users': serializer.data})


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


@api_view(["POST"])
def change_password(request: Request) -> Response:
    user = request.user

    if user.is_anonymous:
        raise exceptions.NotAuthenticated

    data = request.data

    current = data.get('current', '')
    password1 = data.get('password1', '')
    password2 = data.get('password2', '')

    errors = []

    if not current:
        errors.append("Please enter your current password.")

    if not user.check_password(current):
        errors.append("The current password is incorrect.")

    if not password1 or not password2:
        errors.append("Please enter the new password twice.")

    if password1 != password2:
        errors.append("The new passwords don't match.")

    if errors:
        return Response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)

    user.set_password(password1)
    user.save()
    update_session_auth_hash(request, user)

    return Response({"message": "Your password was changed successfully."})
