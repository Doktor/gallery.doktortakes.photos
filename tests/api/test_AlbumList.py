import pytest
from datetime import date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient

from tests.api.album import AlbumFactory


URL = reverse('api_albums')


@pytest.mark.django_db
class TestAlbumList:
    def setup_method(self):
        self.client = APIClient()

    def test__get_album_list__no_albums(self):
        # Act
        response = self.client.get(URL)

        # Assert
        albums = response.data['albums']
        assert albums == []

    def test__get_album_list(self):
        # Arrange
        AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        AlbumFactory(name='Album Name 2', start=date(2020, 12, 31))

        # Act
        response = self.client.get(URL)

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
