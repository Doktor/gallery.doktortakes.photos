from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


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
