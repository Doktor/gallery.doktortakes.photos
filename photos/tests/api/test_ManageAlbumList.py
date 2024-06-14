import pytest
from http import HTTPStatus as Status

from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from photos.api.views.manage import ManageAlbumList
from photos.tests.api.album import AlbumFactory
from photos.tests.api.utils import LicenseFactory, create_superuser, create_user, Level


url = reverse('api_manage_albums')


@pytest.mark.django_db
class TestManageAlbumList:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        cls.factory = APIRequestFactory()
        cls.default_license = LicenseFactory()

    @pytest.mark.parametrize("level", [
        Level.ANONYMOUS,
        Level.USER,
    ])
    def test_post__no_permission__forbidden(self, level: Level):
        # Arrange
        body = {
            # Required fields
            'groups': [],
            'name': 'Album Name',
            'license_id': self.default_license.id,
            'start': '2020-01-01',
            'tags': [],
            'users': [],
        }
        request = self.factory.post(url, data=body)
        force_authenticate(request, user=create_user(level))

        # Act
        response = ManageAlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.FORBIDDEN

    def test_post__top_level_album_name_already_in_use__bad_request(self):
        # Arrange
        album_name = 'Album Name'
        AlbumFactory(name=album_name, parent=None)

        body = {
            'name': album_name,

            # Required fields
            'groups': [],
            'license_id': self.default_license.id,
            'parent': None,
            'start': '2020-01-01',
            'tags': [],
            'users': [],
        }
        request = self.factory.post(url, data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {
            'non_field_errors': ['A top-level album with that name already exists.']}

    def test_post__child_album_name_already_in_use__bad_request(self):
        # Arrange
        parent_album = AlbumFactory(name='Parent Album Name', parent=None)

        child_album_name = 'Child Album Name'
        AlbumFactory(name=child_album_name, parent=parent_album)

        body = {
            'name': child_album_name,
            'parent': parent_album.path,

            # Required fields
            'groups': [],
            'license_id': self.default_license.id,
            'start': '2020-01-01',
            'tags': [],
            'users': [],
        }

        request = self.factory.post(url, data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {
            'non_field_errors': ['An album with that name and parent album already exists.']}

    def test_post__top_level_album__created(self):
        # Arrange
        body = {
            'name': 'Album Name',

            # Required fields
            'groups': [],
            'license_id': self.default_license.id,
            'parent': None,
            'start': '2020-01-01',
            'tags': [],
            'users': [],
        }
        request = self.factory.post(url, data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.CREATED

        actual_album = response.data
        assert actual_album['name'] == 'Album Name'

    def test_post__child_album__created(self):
        # Arrange
        parent_album = AlbumFactory(name='Parent Album Name')

        body = {
            'name': 'Child Album Name',
            'parent': parent_album.path,

            # Required fields
            'groups': [],
            'license_id': self.default_license.id,
            'start': '2024-01-01',
            'tags': [],
            'users': [],
        }
        request = self.factory.post(url, data=body)
        force_authenticate(request, user=create_superuser())

        # Act
        response = ManageAlbumList.as_view()(request)

        # Assert
        assert response.status_code == Status.CREATED

        actual_album = response.data
        assert actual_album['name'] == 'Child Album Name'
