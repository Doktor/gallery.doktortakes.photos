import pytest
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient

from tests.api.utils import AlbumFactory, create_user, Level


URL = reverse('api_manage_albums')


@pytest.mark.django_db
class TestManageAlbumList:
    def setup_method(self):
        self.client = APIClient()

    @pytest.mark.parametrize("level", [
        Level.ANONYMOUS,
        Level.USER,
    ])
    def test_post__no_permission__forbidden(self, level: Level):
        # Arrange
        user = create_user(level)
        self.client.force_authenticate(user=user)

        body = {
            'name': 'Album Name 1',
            'start': '2020-01-01',
            'end': '2020-01-31',
        }

        # Act
        response = self.client.post(URL, data=body)

        # Assert
        assert response.status_code == Status.FORBIDDEN

    def test_post__album_list__top_level_album_name_unavailable__bad_request(self):
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
        response = self.client.post(URL, data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST

    def test_post__album_list__album_name_unavailable__bad_request(self):
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
        response = self.client.post(URL, data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST

    @pytest.mark.parametrize("level", [
        Level.STAFF,
        Level.SUPERUSER,
    ])
    def test_post__album_list__created(self, level: Level):
        # Arrange
        user = create_user(level)
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
        response = self.client.post(URL, data=body)

        # Assert
        assert response.status_code == Status.CREATED

        actual = response.data
        assert actual['name'] == 'Album Name 1'
        assert actual['start'] == '2020-01-01'
        assert actual['end'] == '2020-01-31'
