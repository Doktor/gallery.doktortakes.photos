import pytest
from datetime import date as Date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from photos.api.views import AlbumList
from photos.tests.api.album import AlbumFactory
from photos.tests.api.utils import Level, create_user

url = reverse('api_albums')


@pytest.mark.django_db
class TestAlbumList:
    @classmethod
    def setup_class(cls):
        cls.default_user = create_user(Level.ANONYMOUS)
        cls.factory = APIRequestFactory()

    def test__get_albums_no_albums__ok(self):
        # Arrange
        request = self.factory.get(url)
        force_authenticate(request, user=self.default_user)

        # Act
        response = AlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.OK

        albums = response.data['albums']
        assert albums == []

    def test__get_albums__ok(self):
        # Arrange
        AlbumFactory(name='Album Name 1', start=Date(2024, 1, 1))
        AlbumFactory(name='Album Name 2', start=Date(2024, 12, 31))

        request = self.factory.get(url)
        force_authenticate(request, user=self.default_user)

        # Act
        response = AlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.OK

        actual_albums = response.data['albums']
        assert len(actual_albums) == 2

        actual_album1 = next(filter(lambda a: a['name'] == 'Album Name 1', actual_albums))
        assert actual_album1['name'] == "Album Name 1"
        assert actual_album1['start'] == "2024-01-01"

        actual_album2 = next(filter(lambda a: a['name'] == 'Album Name 2', actual_albums))
        assert actual_album2['name'] == "Album Name 2"
        assert actual_album2['start'] == "2024-12-31"

    def test__get_albums_no_children__ok(self):
        # Arrange
        parent = AlbumFactory(name='Album Name 1')
        AlbumFactory(name='child1', parent=parent)

        request = self.factory.get(url)
        force_authenticate(request, user=self.default_user)

        # Act
        response = AlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.OK

        actual_albums = response.data['albums']
        assert len(actual_albums) == 1

        actual_parent = actual_albums[0]
        assert actual_parent['name'] == "Album Name 1"
