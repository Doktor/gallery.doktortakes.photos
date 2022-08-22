import json
import pytest
from http import HTTPStatus as Status

from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from photos.api.views.manage import ManageAlbumDetail
from photos.models.album import Album, Allow
from photos.tests.api.utils import DjangoUser, Level, create_album, create_user


api_factory = APIRequestFactory()
view = ManageAlbumDetail.as_view()


def get_response(method: str, user: DjangoUser, album: Album, data: dict = None) -> Response:
    if data is None:
        request = api_factory.generic(method, f"/api/manage/albums/{album.path}")
    else:
        encoded = json.dumps(data)
        request = api_factory.generic(
            method, f"/api/manage/albums/{album.path}", data=encoded, content_type="application/json")

    force_authenticate(request, user=user)

    response = view(request, path=album.path)
    response.render()
    return response


parameters = [
    (Level.ANONYMOUS, Allow.PUBLIC, False),
    (Level.ANONYMOUS, Allow.SIGNED_IN, False),
    (Level.ANONYMOUS, Allow.OWNERS, False),
    (Level.ANONYMOUS, Allow.STAFF, False),
    (Level.ANONYMOUS, Allow.SUPERUSER, False),

    (Level.USER, Allow.PUBLIC, False),
    (Level.USER, Allow.SIGNED_IN, False),
    (Level.USER, Allow.OWNERS, False),
    (Level.USER, Allow.STAFF, False),
    (Level.USER, Allow.SUPERUSER, False),

    (Level.OWNER, Allow.PUBLIC, False),
    (Level.OWNER, Allow.SIGNED_IN, False),
    (Level.OWNER, Allow.OWNERS, False),
    (Level.OWNER, Allow.STAFF, False),
    (Level.OWNER, Allow.SUPERUSER, False),

    (Level.STAFF, Allow.PUBLIC, True),
    (Level.STAFF, Allow.SIGNED_IN, True),
    (Level.STAFF, Allow.OWNERS, True),
    (Level.STAFF, Allow.STAFF, True),
    pytest.param(
        Level.STAFF, Allow.SUPERUSER, False,
        marks=pytest.mark.skip("currently broken: need to reevaluate response statuses")),

    (Level.SUPERUSER, Allow.PUBLIC, True),
    (Level.SUPERUSER, Allow.SIGNED_IN, True),
    (Level.SUPERUSER, Allow.OWNERS, True),
    (Level.SUPERUSER, Allow.STAFF, True),
    (Level.SUPERUSER, Allow.SUPERUSER, True),
]


@pytest.mark.django_db
class TestManageAlbumDetailPermissions:
    @pytest.mark.parametrize("user_level, access_level, can_execute", parameters)
    def test_patch__permissions(self, user_level: Level, access_level: Allow, can_execute: bool):
        # Arrange
        user = create_user(user_level)
        album = create_album(access_level, user if user_level == Level.OWNER else None)

        data = {
            "cover": None,
        }

        # Act
        response = get_response("PATCH", user, album, data)

        # Assert
        status = Status.OK if can_execute else Status.FORBIDDEN
        assert response.status_code == status, response.content

    @pytest.mark.parametrize("user_level, access_level, can_execute", parameters)
    def test_put__permissions(self, user_level: Level, access_level: Allow, can_execute: bool):
        # Arrange
        user = create_user(user_level)
        album = create_album(access_level, user if user_level == Level.OWNER else None)

        data = {
            "name": f"{album.name} {album.name}",
            "start": "2019-01-01",
            "tags": [],
            "users": [],
            "groups": [],
            "parent": None,
        }

        # Act
        response = get_response("PUT", user, album, data)

        # Assert
        status = Status.OK if can_execute else Status.FORBIDDEN
        assert response.status_code == status, response.content

    @pytest.mark.parametrize("user_level, access_level, can_execute", parameters)
    def test_delete__permissions(self, user_level: Level, access_level: Allow, can_execute: bool):
        # Arrange
        user = create_user(user_level)
        album = create_album(access_level, user if user_level == Level.OWNER else None)

        # Act
        response = get_response("DELETE", user, album)

        # Assert
        status = Status.NO_CONTENT if can_execute else Status.FORBIDDEN
        assert response.status_code == status, response.content
