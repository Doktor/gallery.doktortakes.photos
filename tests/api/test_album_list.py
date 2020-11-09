import factory
import json
import pytest
from datetime import date, timedelta
from http import HTTPStatus as Status
from unittest import mock

from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient

from photos.api.views import AlbumList
from photos.models import Album
from tests.api.utils import create_user, DjangoUser, Level

view_class = AlbumList
allowed_methods = view_class().allowed_methods

api_factory = APIRequestFactory()
view = view_class.as_view()


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album Name {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    path = factory.LazyAttribute(lambda o: o.slug)

    start = factory.Faker('date_object')
    end = factory.LazyAttribute(lambda o: o.start + timedelta(days=10))

    class Meta:
        model = Album


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


@pytest.mark.django_db
class TestAlbumList:
    @classmethod
    def setup_class(cls):
        cls.factory = APIRequestFactory()

    def setup_method(self):
        self.client = APIClient()

    def test_get_album_list__no_albums(self):
        # Arrange
        client = APIClient()

        # Act
        response = self.client.get('/api/albums/')

        # Assert
        albums = response.data['albums']
        assert albums == []

    def test_get_album_list(self):
        # Arrange
        album1 = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        album2 = AlbumFactory(name='Album Name 2', start=date(2020, 12, 31))

        # Act
        response = self.client.get('/api/albums/')

        # Assert
        assert response.status_code == Status.OK

        albums = response.data['albums']
        assert len(albums) == 2

        album1 = next(filter(lambda a: a['name'] == 'Album Name 1', albums))
        album2 = next(filter(lambda a: a['name'] == 'Album Name 2', albums))

        assert "Album Name 1" == album1['name']
        assert "2020-01-01" == album1['start']

        assert "Album Name 2" == album2['name']
        assert "2020-12-31" == album2['start']

    def test_post_album_list__no_permission(self):
        # Arrange
        user = create_user(Level.USER)
        self.client.force_authenticate(user=user)

        body = {
            'name': 'Album Name 1',
            'start': '2020-01-01',
            'end': '2020-01-31',
        }

        # Act
        response = self.client.post('/api/albums/', data=body)

        # Assert
        assert response.status_code == Status.FORBIDDEN

    def test_post_album_list__top_level_album_name_unavailable(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user=user)

        album = AlbumFactory(name='Album Name 1', parent=None)

        body = {
            'name': album.name,
            'parent': None,
            'start': '2020-01-01',

            'tags': [],
            'users': [],
            'groups': [],
        }

        # Act
        response = self.client.post('/api/albums/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST

    def test_post_album_list__album_name_unavailable(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user=user)

        parent = AlbumFactory(name='Parent Album', parent=None)
        album = AlbumFactory(name='Album Name 1', parent=parent)

        body = {
            'name': album.name,
            'parent': parent.path,
            'start': '2020-01-01',

            'tags': [],
            'users': [],
            'groups': [],
        }

        # Act
        response = self.client.post('/api/albums/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST

    def test_post_album_list(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user=user)

        body = {
            'name': 'Album Name 1',
            'start': '2020-01-01',
            'end': '2020-01-31',
            'parent': None,

            'tags': [],
            'users': [],
            'groups': [],
        }

        # Act
        response = self.client.post('/api/albums/', data=body)

        # Assert
        assert response.status_code == Status.CREATED

        actual = response.data
        assert actual['name'] == 'Album Name 1'
        assert actual['start'] == '2020-01-01'
        assert actual['end'] == '2020-01-31'
