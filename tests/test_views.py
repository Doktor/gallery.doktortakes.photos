from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.files import File
from django.db.models.signals import post_save
from django.test import RequestFactory
from django.urls import reverse

from photos import views
from photos.models import Album, Photo
from photos.models.utils import generate_md5_hash
from photos.settings import INDEX_ALBUMS, INDEX_FEATURED_PHOTOS

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


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album {n} Title")
    start = factory.Faker('date')

    class Meta:
        model = Album


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
