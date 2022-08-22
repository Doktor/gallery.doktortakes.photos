import pytest
from datetime import date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient

from photos.tests.api.utils import AlbumFactory, create_user, Level


URL = lambda path: reverse('api_manage_album', kwargs={'path': path})


def create_request_body(**kwargs):
    return {
        'parent': None,

        'tags': [],
        'users': [],
        'groups': [],

        **kwargs,
    }


@pytest.mark.django_db
class TestManageAlbumDetail:
    def setup_method(self):
        self.client = APIClient()

    def test_put__missing_name(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = create_request_body(start='2020-12-31')

        # Act
        response = self.client.put(URL(album.path), data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'name': ['This field is required.']}

    def test_put__missing_start_date(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = create_request_body(name='Album Name 1')

        # Act
        response = self.client.put(URL(album.path), data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'start': ['This field is required.']}

    def test_put__invalid_parent(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(
            name='Album Name 1', start=date(2020, 1, 1), parent=None)
        body = create_request_body(
            name=album.name, start=album.start, parent=album.path)

        # Act
        response = self.client.put(URL(album.path), data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {
            'non_field_errors': ['An album can\'t be its own parent.']}

    def test_put__start_date_after_end_date(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = create_request_body(
            name='Album Name 1', start='2020-01-01', end='2019-12-31', parent='album-name-1')

        # Act
        response = self.client.put(URL(album.path), data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'non_field_errors':
            ['The end date should be later than the start date.']}

    def test_put(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = create_request_body(name='Album Name 2', start='2010-12-31')

        # Act
        response = self.client.put(URL(album.path), data=body)

        # Assert
        assert response.status_code == Status.OK

        actual = response.data
        assert actual['name'] == 'Album Name 2'
        assert actual['start'] == '2010-12-31'

    def test_delete__no_permission(self):
        # Arrange
        user = create_user(Level.USER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        # Act
        response = self.client.delete(URL(album.path))

        # Assert
        assert response.status_code == Status.FORBIDDEN

        content = response.content.decode('utf-8')
        assert album.name not in content
        assert album.path not in content

    def test_delete(self):
        # Arrange
        user = create_user(Level.SUPERUSER)
        self.client.force_authenticate(user)

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        # Act
        response = self.client.delete(URL(album.path))

        # Assert
        assert response.status_code == Status.NO_CONTENT
        assert response.data is None
