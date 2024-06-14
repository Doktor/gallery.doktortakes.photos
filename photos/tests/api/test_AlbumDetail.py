import pytest
from datetime import date as Date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from photos.api.views import AlbumDetail
from photos.models.album import Allow
from photos.tests.api.utils import AlbumFactory, Level, create_album, create_anonymous_user, create_user


def url(path):
    return reverse("api_album", kwargs={"path": path})


@pytest.mark.django_db
class TestAlbumDetail:
    @classmethod
    def setup_class(cls):
        cls.factory = APIRequestFactory()

    def setup_method(self):
        self.client = APIClient()

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
        (Level.STAFF, Allow.OWNERS, True),
        (Level.STAFF, Allow.STAFF, True),
        (Level.STAFF, Allow.SUPERUSER, False),

        (Level.SUPERUSER, Allow.PUBLIC, True),
        (Level.SUPERUSER, Allow.SIGNED_IN, True),
        (Level.SUPERUSER, Allow.OWNERS, True),
        (Level.SUPERUSER, Allow.STAFF, True),
        (Level.SUPERUSER, Allow.SUPERUSER, True),
    ])
    def test__get_album__permissions(self, user_level: Level, album_level: Allow, can_access: bool):
        # Arrange
        user = create_user(user_level)
        self.client.force_authenticate(user)

        album = create_album(album_level, user if user_level == Level.OWNER else None)

        # Act
        response = self.client.get(url(album.path))

        # Assert
        if can_access:
            assert response.status_code == Status.OK, response.content
        else:
            assert response.status_code == Status.NOT_FOUND, response.content

    def test__get_album__not_found(self):
        # Arrange
        path = "test_get_album_not_found"

        request = self.factory.get(url(path))
        force_authenticate(request, user=create_anonymous_user())

        # Act
        response = AlbumDetail.as_view()(request, path)

        # Assert
        assert response.status_code == Status.NOT_FOUND

    def test__get_album(self):
        # Arrange
        album = AlbumFactory(
            name="test_get_album",
            start=Date(2024, 1, 1),
            end=Date(2024, 1, 31),
            parent=None)

        request = self.factory.get(url(album.path))
        force_authenticate(request, user=create_anonymous_user())

        # Act
        response = AlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.OK

        actual_album = response.data["album"]
        assert actual_album["name"] == "test_get_album"
        assert actual_album["start"] == "2024-01-01"
        assert actual_album["end"] == "2024-01-31"
        assert actual_album["parent"] is None

        actual_children = response.data["children"]
        assert actual_children == []

    def test__get_album_with_children(self):
        # Arrange
        album = AlbumFactory(name="test_get_album_with_children")

        AlbumFactory(name="child1", start=Date(2024, 1, 1), parent=album)
        AlbumFactory(name="child2", start=Date(2024, 2, 1), parent=album)

        request = self.factory.get(url(album.path))
        force_authenticate(request, user=create_anonymous_user())

        # Act
        response = AlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.OK

        actual_album = response.data["album"]
        assert actual_album["name"] == "test_get_album_with_children"

        actual_children = response.data["children"]
        assert len(actual_children) == 2

        actual_child1 = actual_children[0]
        assert actual_child1["name"] == "child1"
        assert actual_child1["start"] == "2024-01-01"

        actual_child2 = actual_children[1]
        assert actual_child2["name"] == "child2"
        assert actual_child2["start"] == "2024-02-01"
