import pytest
from datetime import date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient

from photos.models.album import Allow
from photos.tests.api.utils import AlbumFactory, Level, create_album, create_user

URL = lambda path: reverse('api_album', kwargs={'path': path})


@pytest.mark.django_db
class TestAlbumDetail:
    def setup_method(self):
        self.client = APIClient()

    @staticmethod
    def create_request_body(**kwargs):
        return {
            'parent': None,

            'tags': [],
            'users': [],
            'groups': [],

            **kwargs,
        }

    @pytest.mark.parametrize("user_level, album_level, can_access", [
        (Level.ANONYMOUS, Allow.PUBLIC, True),
        (Level.ANONYMOUS, Allow.SIGNED_IN, False),
        (Level.ANONYMOUS, Allow.OWNERS, False),
        (Level.ANONYMOUS, Allow.STAFF, False),
        (Level.ANONYMOUS, Allow.SUPERUSER, False),

        (Level.USER, Allow.PUBLIC, True),
        (Level.USER, Allow.SIGNED_IN, True),
        (Level.USER, Allow.OWNERS, False),
        (Level.USER, Allow.STAFF, False),
        (Level.USER, Allow.SUPERUSER, False),

        (Level.OWNER, Allow.PUBLIC, True),
        (Level.OWNER, Allow.SIGNED_IN, True),
        (Level.OWNER, Allow.OWNERS, True),
        (Level.OWNER, Allow.STAFF, False),
        (Level.OWNER, Allow.SUPERUSER, False),

        (Level.STAFF, Allow.PUBLIC, True),
        (Level.STAFF, Allow.SIGNED_IN, True),
        pytest.param(
            Level.STAFF, Allow.OWNERS, True,
            marks=pytest.mark.skip("currently broken due to a bug: see issue #163")),
        (Level.STAFF, Allow.STAFF, True),
        (Level.STAFF, Allow.SUPERUSER, False),

        (Level.SUPERUSER, Allow.PUBLIC, True),
        (Level.SUPERUSER, Allow.SIGNED_IN, True),
        (Level.SUPERUSER, Allow.OWNERS, True),
        (Level.SUPERUSER, Allow.STAFF, True),
        (Level.SUPERUSER, Allow.SUPERUSER, True),
    ])
    def test_get__permissions(self, user_level: Level, album_level: Allow, can_access: bool):
        # Arrange
        user = create_user(user_level)
        self.client.force_authenticate(user)

        album = create_album(album_level, user if user_level == Level.OWNER else None)

        # Act
        response = self.client.get(URL(album.path))

        # Assert
        if can_access:
            assert response.status_code == Status.OK, response.content
        else:
            assert response.status_code == Status.NOT_FOUND, response.content

    def test_get__not_found(self):
        # Act
        response = self.client.get(URL("path"))

        # Assert
        assert response.status_code == Status.NOT_FOUND

    def test_get(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1), parent=None)

        # Act
        response = self.client.get(URL(album.path))

        # Assert
        assert response.status_code == Status.OK

        actual = response.data
        assert actual['name'] == album.name
        assert actual['start'] == '2020-01-01'
        assert actual['parent'] is None
