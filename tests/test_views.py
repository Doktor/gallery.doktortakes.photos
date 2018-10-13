from django.contrib.auth.models import AnonymousUser, User, Group
from django.core.cache import cache
from django.core.files import File
from django.db.models.signals import post_save
from django.http import Http404
from django.templatetags.static import static
from django.test import RequestFactory
from django.urls import reverse

from photos import views
from photos.models import Album, Photo, Tag
from photos.models.utils import generate_md5_hash
from photos.settings import INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE

import datetime
import factory
import faker
import PIL.Image
import PIL.ImageColor
import pytest
import pytz
import random
from http import HTTPStatus
from io import BytesIO


fake = faker.Faker()
methods = ('get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace')


# Factory helpers


colors = tuple(PIL.ImageColor.colormap.keys())
generated = []


def generate_image():
    while True:
        width = random.randint(500, 1500)
        height = random.randint(500, 1500)
        color = random.choice(colors)

        image = (width, height, color)

        if image not in generated:
            generated.append(image)
            break

    thumb = PIL.Image.new('RGB', (width, height), color)
    data = BytesIO()
    data.name = 'test.jpg'
    thumb.save(data, format='JPEG')

    return data


# Factories


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    password = factory.Faker('password', length=8, digits=True, lower_case=True)

    is_staff = False

    class Meta:
        model = User


class GroupFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Group {n}")

    class Meta:
        model = Group


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album {n} Title")
    start = factory.Faker('date')

    class Meta:
        model = Album


class TagFactory(factory.DjangoModelFactory):
    slug = factory.Sequence(lambda n: f"tag-{n}-slug")

    class Meta:
        model = Tag


class PhotoFactory:
    def __new__(cls, *args, **kwargs) -> Photo:
        photo = Photo(**kwargs)

        image = generate_image()
        photo.md5 = generate_md5_hash(File(image))
        cache.set(photo.md5, image, 60 * 60 * 24)

        with factory.django.mute_signals(post_save):
            photo.save()

        photo.taken = kwargs.pop('taken', None) or fake.date_time(tzinfo=pytz.utc)
        photo.edited = kwargs.pop('edited', None) or fake.date_time(tzinfo=pytz.utc)

        photo.image.save(image.name, File(image), save=False)
        photo.thumbnail.save(image.name, File(image), save=False)
        photo.square_thumbnail.save(image.name, File(image), save=False)

        with factory.django.mute_signals(post_save):
            photo.save()

        return photo


# Test helpers


@pytest.mark.skip('not a test')
def test_allowed_methods(view, url, allowed_methods):
    rf = RequestFactory()

    for method in methods:
        request = rf.generic(method, reverse(url))
        request.user = AnonymousUser()

        response = view(request)

        if method in allowed_methods:
            assert response.status_code == HTTPStatus.OK
        else:
            assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


# Tests


@pytest.mark.django_db
class TestIndex:
    def test_allowed_methods(self):
        test_allowed_methods(views.index, 'index', ('get',))

    def test_no_albums_exist(self, rf):
        request = rf.get(reverse('index'))
        request.user = AnonymousUser()

        response = views.index(request)
        content = response.content.decode('utf-8')
        assert "No albums found" in content

    def test_one_album_exists(self, rf):
        request = rf.get(reverse('index'))
        request.user = AnonymousUser()

        album = AlbumFactory()

        response = views.index(request)
        content = response.content.decode('utf-8')
        assert "No albums found" not in content
        assert "View more albums" not in content
        assert album.name in content

    def test_many_albums_exist(self, rf):
        request = rf.get(reverse('index'))
        request.user = AnonymousUser()

        start = datetime.date(year=2018, month=1, day=1)
        album = AlbumFactory(start=start)

        for _ in range(INDEX_ALBUMS):
            start = start.replace(day=start.day + 1)
            last = AlbumFactory(start=start)

        response = views.index(request)
        content = response.content.decode('utf-8')
        assert "View more albums" in content
        assert album.name not in content
        assert last.name in content


@pytest.mark.django_db
class TestFeatured:
    featured = dict(rating=5, sidecar_exists=True)

    def test_allowed_methods(self):
        test_allowed_methods(views.featured, 'index', ('get',))

    def test_no_featured_photos_exist(self, rf):
        request = rf.get(reverse('featured'))
        request.user = AnonymousUser()

        response = views.featured(request)
        content = response.content.decode('utf-8')
        assert "No featured photos found" in content

    def test_some_featured_photos_exist(self, rf):
        request = rf.get(reverse('featured'))
        request.user = AnonymousUser()

        album = AlbumFactory(hidden=False)

        for _ in range(INDEX_FEATURED_PHOTOS // 2):
            last = PhotoFactory(album=album, **self.featured)

        response = views.featured(request)
        content = response.content.decode('utf-8')
        assert "No featured photos found" not in content
        assert last.thumbnail.url in content

    def test_many_featured_photos_exist(self, rf):
        request = rf.get(reverse('featured'))
        request.user = AnonymousUser()

        album = AlbumFactory(hidden=False)
        taken = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.utc)

        first = PhotoFactory(album=album, taken=taken, **self.featured)

        for _ in range(INDEX_FEATURED_PHOTOS):
            taken = taken + datetime.timedelta(seconds=1)
            last = PhotoFactory(album=album, taken=taken, **self.featured)

        response = views.featured(request)
        content = response.content.decode('utf-8')
        assert first.thumbnail.url not in content
        assert last.thumbnail.url in content


@pytest.mark.django_db
class TestViewAlbums:
    def get_response(self, user=AnonymousUser(), data=None):
        rf = RequestFactory()

        request = rf.get(reverse('albums'), data=data)
        request.user = user

        response = views.view_albums(request)
        return response.content.decode('utf-8')

    # Tests

    def test_allowed_methods(self):
        test_allowed_methods(views.view_albums, 'albums', ('get',))

    def test_anonymous_user_cannot_see_hidden_albums(self):
        album = AlbumFactory(hidden=True)

        content = self.get_response()
        assert album.name not in content

    def test_anonymous_user_can_see_public_albums(self):
        album = AlbumFactory()

        content = self.get_response()
        assert album.name in content

    def test_user_can_see_private_albums_only_when_query_string_is_set(self):
        user = UserFactory()
        group = GroupFactory()
        user.groups.add(group)

        album = AlbumFactory()
        album.users.add(user)

        album_2 = AlbumFactory()
        album_2.groups.add(group)

        content = self.get_response(user=user)
        assert album.name not in content
        assert album_2.name not in content

        content = self.get_response(user=user, data={'hidden': True})
        assert album.name in content
        assert album_2.name in content

    def test_user_cannot_see_other_private_albums(self):
        user = UserFactory()
        user_2 = UserFactory()
        group = GroupFactory()

        album = AlbumFactory()
        album.users.add(user_2)

        album_2 = AlbumFactory()
        album_2.groups.add(group)

        content = self.get_response(user=user)
        assert album.name not in content
        assert album_2.name not in content

    @pytest.mark.xfail(reason="staff users can see private albums without the query string")
    def test_staff_user_can_see_private_albums_only_when_query_string_is_set(self):
        user = UserFactory(is_staff=True)
        other = UserFactory()
        group = GroupFactory()

        album = AlbumFactory()
        album.users.add(other)

        album_2 = AlbumFactory()
        album_2.groups.add(group)

        content = self.get_response(user=user)
        assert album.name not in content
        assert album_2.name not in content

        content = self.get_response(user=user, data={'hidden': True})
        assert album.name in content
        assert album_2.name in content

    def test_all_albums_appear_when_many_albums_exist(self):
        """Extra albums past the per-page limit are hidden by JS and can be
        shown with the pagination controls."""
        start = datetime.date(year=2018, month=1, day=1)
        first = AlbumFactory(start=start)

        for _ in range(ITEMS_PER_PAGE):
            start = start.replace(day=start.day + 1)
            last = AlbumFactory(start=start)

        content = self.get_response()
        assert first.name in content
        assert last.name in content


@pytest.mark.skip
class TestViewAlbum:
    pass


@pytest.mark.django_db
class TestViewTags:
    def get_response(self, user=AnonymousUser()):
        rf = RequestFactory()

        request = rf.get(reverse('tags'))
        request.user = user

        response = views.view_tags(request)
        return response.content.decode('utf-8')

    # Tests

    def test_allowed_methods(self):
        test_allowed_methods(views.view_tags, 'tags', ('get',))

    def test_no_tags_exist(self):
        content = self.get_response()
        assert "No tags found" in content

    def test_tags_exist(self):
        tags = TagFactory.create_batch(10)

        content = self.get_response()
        assert "No tags found" not in content
        assert all(tag.slug in content for tag in tags)
        assert all(tag.get_absolute_url() in content for tag in tags)

    def test_many_tags_exist(self):
        """All tags should be displayed, regardless of how many there are."""
        tags = TagFactory.create_batch(1000)

        content = self.get_response()
        assert all(tag.slug in content for tag in tags)


@pytest.mark.django_db
class TestViewTag:
    def get_response(self, slug, user=AnonymousUser()):
        rf = RequestFactory()

        request = rf.get(reverse('tag', kwargs={'slug': slug}))
        request.user = user

        response = views.view_tag(request, slug)
        return response.content.decode('utf-8')

    # Tests

    def test_tag_that_does_not_exist(self):
        with pytest.raises(Http404):
            self.get_response(None)

    def test_tag_with_no_albums(self):
        tag = TagFactory(description="Example description")

        content = self.get_response(tag.slug)
        assert tag.slug in content
        assert tag.description in content
        assert static("images/cover-placeholder.png") in content
        assert "No albums were found with this tag" in content

    def test_tag_with_one_album(self):
        tag = TagFactory()

        album = AlbumFactory()
        album.tags.add(tag)

        content = self.get_response(tag.slug)
        assert "1 album" in content
        assert album.name in content

    def test_tag_with_many_albums(self):
        tag = TagFactory()

        albums = AlbumFactory.create_batch(10)
        for album in albums:
            album.tags.add(tag)

        content = self.get_response(tag.slug)
        assert "10 albums" in content
        assert all(album.name in content for album in albums)

    @pytest.mark.skip(reason="no pagination implemented")
    def test_tag_with_more_albums_than_page_limit(self):
        tag = TagFactory()

        albums = AlbumFactory.create_batch(50)
        for album in albums:
            album.tags.add(tag)

    def test_view_does_not_show_albums_with_other_tags(self):
        tag = TagFactory()

        tag_2 = TagFactory()
        album = AlbumFactory()
        album.tags.add(tag_2)

        content = self.get_response(tag.slug)
        assert "No albums were found with this tag" in content
