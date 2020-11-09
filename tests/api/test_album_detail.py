import factory
import json
import pytest
from datetime import date, timedelta
from http import HTTPStatus as Status

from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient

from photos.api.views import AlbumDetail
from photos.models import Album
from photos.models.album import Allow
from tests.api.utils import create_album, create_user, DjangoUser, Level

view_class = AlbumDetail
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


def get_response(method: str, user: DjangoUser, album: Album, data: dict = None) -> Response:
    if data is None:
        request = api_factory.generic(method, f"/api/albums/{album.path}")
    else:
        encoded = json.dumps(data)
        request = api_factory.generic(
            method, f"/api/albums/{album.path}", data=encoded, content_type="application/json")

    request.user = user

    response: Response = view(request, path=album.path)
    response.render()
    return response


# Assert helper functions


def assert_patch(user: DjangoUser, album: Album, expected_status_code: Status):
    data = {
        "cover": None,
    }
    response = get_response("PATCH", user, album, data)
    assert response.status_code == expected_status_code, response.content


def assert_put(user: DjangoUser, album: Album, expected_status_code: Status):
    data = {
        "name": f"{album.name} {album.name}",
        "start": "2019-01-01",
        "tags": [],
        "users": [],
        "groups": [],
        "parent": None,
    }
    response = get_response("PUT", user, album, data)
    assert response.status_code == expected_status_code, response.content


def assert_delete(user: DjangoUser, album: Album, expected_status_code: Status):
    response = get_response("DELETE", user, album)
    assert response.status_code == expected_status_code, response.content


# Test class


@pytest.mark.django_db
class TestAlbumDetailPermissions:
    @pytest.mark.parametrize("user_level, access_level, visible", [
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
            Level.STAFF, Allow.OWNERS, True, marks=pytest.mark.skip("Unexpected behavior")),
        (Level.STAFF, Allow.STAFF, True),
        (Level.STAFF, Allow.SUPERUSER, False),

        (Level.SUPERUSER, Allow.PUBLIC, True),
        (Level.SUPERUSER, Allow.SIGNED_IN, True),
        (Level.SUPERUSER, Allow.OWNERS, True),
        (Level.SUPERUSER, Allow.STAFF, True),
        (Level.SUPERUSER, Allow.SUPERUSER, True),
    ])
    def test_hide_album(self, user_level: Level, access_level: Allow, visible: bool):
        """Tests whether a user can see an album with the given access level."""
        user = create_user(user_level)
        album = create_album(access_level, user if user_level == Level.OWNER else None)

        for method in ("GET", "HEAD", "PATCH", "PUT", "DELETE"):
            response = get_response(method, user, album)

            if visible:
                assert response.status_code != Status.NOT_FOUND, response.content
            else:
                assert response.status_code == Status.NOT_FOUND, response.content

    # GET, HEAD

    @pytest.mark.parametrize("user_level, access_level, expected_status_code", [
        (Level.ANONYMOUS, Allow.PUBLIC, Status.OK),
        (Level.ANONYMOUS, Allow.SIGNED_IN, Status.NOT_FOUND),
        (Level.ANONYMOUS, Allow.OWNERS, Status.NOT_FOUND),
        (Level.ANONYMOUS, Allow.STAFF, Status.NOT_FOUND),
        (Level.ANONYMOUS, Allow.SUPERUSER, Status.NOT_FOUND),

        (Level.USER, Allow.PUBLIC, Status.OK),
        (Level.USER, Allow.SIGNED_IN, Status.OK),
        (Level.USER, Allow.OWNERS, Status.NOT_FOUND),
        (Level.USER, Allow.STAFF, Status.NOT_FOUND),
        (Level.USER, Allow.SUPERUSER, Status.NOT_FOUND),

        (Level.OWNER, Allow.PUBLIC, Status.OK),
        (Level.OWNER, Allow.SIGNED_IN, Status.OK),
        (Level.OWNER, Allow.OWNERS, Status.OK),
        (Level.OWNER, Allow.STAFF, Status.NOT_FOUND),
        (Level.OWNER, Allow.SUPERUSER, Status.NOT_FOUND),

        (Level.STAFF, Allow.PUBLIC, Status.OK),
        (Level.STAFF, Allow.SIGNED_IN, Status.OK),
        pytest.param(
            Level.STAFF, Allow.OWNERS, Status.OK, marks=pytest.mark.skip("Unexpected behavior")),
        (Level.STAFF, Allow.STAFF, Status.OK),
        (Level.STAFF, Allow.SUPERUSER, Status.NOT_FOUND),

        (Level.SUPERUSER, Allow.PUBLIC, Status.OK),
        (Level.SUPERUSER, Allow.SIGNED_IN, Status.OK),
        (Level.SUPERUSER, Allow.OWNERS, Status.OK),
        (Level.SUPERUSER, Allow.STAFF, Status.OK),
        (Level.SUPERUSER, Allow.SUPERUSER, Status.OK),
    ])
    def test_safe_methods(self, user_level: Level, access_level: Allow,
                          expected_status_code: Status):
        user = create_user(user_level)
        album = create_album(access_level, user if user_level == Level.OWNER else None)

        for method in ("GET", "HEAD"):
            response = get_response(method, user, album)
            assert response.status_code == expected_status_code, response.content

    # PATCH, PUT, DELETE

    @pytest.mark.parametrize("user_level, access_level, expected_status_code", [
        # Anonymous users are never allowed
        (Level.ANONYMOUS, Allow.PUBLIC, Status.FORBIDDEN),

        # Regular users are never allowed
        (Level.USER, Allow.PUBLIC, Status.FORBIDDEN),
        (Level.USER, Allow.SIGNED_IN, Status.FORBIDDEN),

        # Album owners are never allowed
        (Level.OWNER, Allow.PUBLIC, Status.FORBIDDEN),
        (Level.OWNER, Allow.SIGNED_IN, Status.FORBIDDEN),
        (Level.OWNER, Allow.OWNERS, Status.FORBIDDEN),

        # Staff are always allowed
        (Level.STAFF, Allow.PUBLIC, Status.OK),
        (Level.STAFF, Allow.SIGNED_IN, Status.OK),
        pytest.param(
            Level.STAFF, Allow.OWNERS, Status.OK, marks=pytest.mark.skip("Unexpected behavior")),
        (Level.STAFF, Allow.STAFF, Status.OK),

        # Superusers are always allowed
        (Level.SUPERUSER, Allow.PUBLIC, Status.OK),
        (Level.SUPERUSER, Allow.SIGNED_IN, Status.OK),
        (Level.SUPERUSER, Allow.OWNERS, Status.OK),
        (Level.SUPERUSER, Allow.STAFF, Status.OK),
        (Level.SUPERUSER, Allow.SUPERUSER, Status.OK),
    ])
    def test_unsafe_methods(self, user_level: Level, access_level: Allow,
                            expected_status_code: Status):
        """Tests if a user can make unsafe requests for albums they have access to."""
        user = create_user(user_level)
        is_owner = user_level == Level.OWNER

        for method in (assert_patch, assert_put):
            album = create_album(access_level, user if is_owner else None)
            method(user, album, expected_status_code)

        album = create_album(access_level, user if is_owner else None)
        assert_delete(user, album,
                      Status.NO_CONTENT if expected_status_code == Status.OK else expected_status_code)

    # OPTIONS, POST

    @pytest.mark.parametrize("method", ["OPTIONS", "POST"])
    def test_method_not_allowed(self, method):
        response = get_response(method, create_user(Level.SUPERUSER), create_album(Allow.PUBLIC))
        assert response.status_code == Status.METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestAlbumDetail:
    @classmethod
    def setup_class(cls):
        cls.factory = APIRequestFactory()

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

    def test_get_album_detail__not_found(self):
        # Act
        response = self.client.get('/api/albums/test-album/')

        # Assert
        assert response.status_code == Status.NOT_FOUND

    def test_get_album_detail(self):
        # Arrange
        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1), parent=None)

        # Act
        response = self.client.get(f'/api/albums/{album.path}/')

        # Assert
        assert response.status_code == Status.OK

        actual = response.data
        assert actual['name'] == album.name
        assert actual['start'] == '2020-01-01'
        assert actual['parent'] == None

    def test_put_album_detail__missing_name(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = self.create_request_body(start='2020-12-31')

        # Act
        response = self.client.put(f'/api/albums/{album.path}/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'name': ['This field is required.']}

    def test_put_album_detail__missing_start_date(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = self.create_request_body(name='Album Name 1')

        # Act
        response = self.client.put(f'/api/albums/{album.path}/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'start': ['This field is required.']}

    def test_put_album_detail__invalid_parent(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(
            name='Album Name 1', start=date(2020, 1, 1), parent=None)
        body = self.create_request_body(
            name=album.name, start=album.start, parent=album.path)

        # Act
        response = self.client.put(f'/api/albums/{album.path}/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {
            'non_field_errors': ['An album can\'t be its own parent.']}

    def test_put_album_detail__start_date_after_end_date(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = self.create_request_body(
            name='Album Name 1', start='2020-01-01', end='2019-12-31', parent='album-name-1')

        # Act
        response = self.client.put(f'/api/albums/{album.path}/', data=body)

        # Assert
        assert response.status_code == Status.BAD_REQUEST
        assert response.data == {'non_field_errors':
            ['The end date should be later than the start date.']}

    def test_put_album_detail(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))
        body = self.create_request_body(name='Album Name 2', start='2010-12-31')

        # Act
        response = self.client.put(f'/api/albums/{album.path}/', data=body)

        # Assert
        assert response.status_code == Status.OK

        actual = response.data
        assert actual['name'] == 'Album Name 2'
        assert actual['start'] == '2010-12-31'

    def test_delete_album_detail__no_permission(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.USER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        # Act
        response = self.client.delete(f'/api/albums/{album.path}/')

        # Assert
        assert response.status_code == Status.FORBIDDEN

        content = response.content.decode('utf-8')
        assert album.name not in content
        assert album.path not in content

    def test_delete_album_detail(self):
        # Arrange
        self.client.force_authenticate(user=create_user(Level.SUPERUSER))

        album = AlbumFactory(name='Album Name 1', start=date(2020, 1, 1))

        # Act
        response = self.client.delete(f'/api/albums/{album.path}/')

        # Assert
        assert response.status_code == Status.NO_CONTENT
        assert response.data is None
