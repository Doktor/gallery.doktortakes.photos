import pytest
from datetime import date
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from photos.api.views.manage import ManageAlbumDetail
from photos.tests.api.album import AlbumFactory
from photos.tests.api.utils import LicenseFactory, create_standard_user, create_superuser


url = lambda path: reverse('api_manage_album', kwargs={'path': path})


@pytest.mark.django_db
class TestManageAlbumDetail:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        cls.factory = APIRequestFactory()
        cls.default_license = LicenseFactory()

    def setup_method(self):
        self.client = APIClient()

    def create_request_body(self, **kwargs):
        return {
            'license_id': self.default_license.id,
            'parent': None,

            'tags': [],
            'users': [],
            'groups': [],

            **kwargs,
        }

    def test_put__missing_name__bad_request(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        body = self.create_request_body(start='2020-12-31')
        request = self.factory.put(url(album.path), data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'name': ['This field is required.']}

    def test_put__missing_start_date__bad_request(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        body = self.create_request_body(name='Album Name 1')
        request = self.factory.put(url(album.path), data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'start': ['This field is required.']}

    def test_put__parent_is_self__bad_request(self):
        # Arrange
        album = AlbumFactory(
            name='Album Name 1', start=date(2020, 1, 1), parent=None)

        body = self.create_request_body(
            name=album.name, start=album.start, parent=album.path)
        request = self.factory.put(url(album.path), data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {
            'non_field_errors': ['An album can\'t be its own parent.']}

    def test_put__start_date_after_end_date__bad_request(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        body = self.create_request_body(
            name='Album Name 1', start='2020-01-01', end='2019-12-31', parent='album-name-1')
        request = self.factory.put(url(album.path), data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'non_field_errors':
            ['The end date should be later than the start date.']}

    def test_put(self):
        # Arrange
        album = AlbumFactory(name='Original Album Name', start=date(2024, 1, 1))

        body = self.create_request_body(name='Updated Album Name', start='2024-12-31')
        request = self.factory.put(url(album.path), data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.OK

        actual_album = response.data['album']
        assert actual_album['name'] == 'Updated Album Name'
        assert actual_album['start'] == '2024-12-31'

    def test_delete__no_permission__forbidden(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        request = self.factory.delete(url(album.path))
        force_authenticate(request, user=create_standard_user())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.FORBIDDEN

        response.render()
        content = response.content.decode('utf-8')
        assert album.name not in content
        assert album.path not in content

    def test_delete__ok(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        request = self.factory.delete(url(album.path))
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumDetail.as_view()(request, album.path)

        # Assert
        assert response.status_code == Status.NO_CONTENT
        assert response.data is None
