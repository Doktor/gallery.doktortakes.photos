import pytest
from datetime import date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient

from tests.api.utils import AlbumFactory


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
