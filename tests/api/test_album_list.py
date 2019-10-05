import json
import pytest
from http import HTTPStatus as Status

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from photos.api.views import AlbumList
from tests.api.utils import create_user, DjangoUser, Level

view_class = AlbumList
allowed_methods = view_class().allowed_methods

api_factory = APIRequestFactory()
view = view_class.as_view()


def get_status_code(method: str, user: DjangoUser, data: dict = None) -> int:
    if data is None:
        request = api_factory.generic(method, f"/api/albums/")
    else:
        encoded = json.dumps(data)
        request = api_factory.generic(
            method, f"/api/albums/", data=encoded, content_type="application/json")

    request.user = user

    response: Response = view(request)
    response.render()
    return response.status_code


@pytest.mark.django_db
class TestAlbumListPermission:
    @pytest.mark.parametrize("user_level, expected_status_code", [
        (Level.ANONYMOUS, Status.OK),
        (Level.USER, Status.OK),
        (Level.STAFF, Status.OK),
        (Level.SUPERUSER, Status.OK),
    ])
    def test_safe_methods(self, user_level: Level, expected_status_code: Status):
        """Tests whether a user can see an album with the given access level."""
        for method in ("GET", "HEAD"):
            assert get_status_code(method, create_user(user_level)) == expected_status_code

    @pytest.mark.parametrize("user_level, expected_status_code", [
        (Level.ANONYMOUS, Status.FORBIDDEN),
        (Level.USER, Status.FORBIDDEN),
        (Level.STAFF, Status.CREATED),
        (Level.SUPERUSER, Status.CREATED),
    ])
    def test_post(self, user_level: Level, expected_status_code: Status):
        """Tests whether a user can see an album with the given access level."""
        data = {
            "name": "Album 1 Name",
            "start": "2019-01-01",
            "tags": [],
            "users": [],
            "groups": [],
            "parent": None,
        }

        assert get_status_code("POST", create_user(user_level), data) == expected_status_code

    @pytest.mark.parametrize("method", ["OPTIONS", "PATCH", "PUT", "DELETE"])
    def test_method_not_allowed(self, method):
        assert get_status_code(method, create_user(Level.SUPERUSER)) == Status.METHOD_NOT_ALLOWED
