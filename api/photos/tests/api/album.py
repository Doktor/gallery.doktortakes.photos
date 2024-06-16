import factory
from datetime import timedelta

from django.utils.text import slugify

from photos.models import Album
from photos.models.album import Allow
from photos.tests.api.utils import DjangoUser


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album Name {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    path = factory.LazyAttribute(lambda o: o.slug)

    start = factory.Faker('date_object')

    class Meta:
        model = Album


def create_album(access_level: Allow, user: DjangoUser = None):
    album = AlbumFactory(access_level=access_level)

    if user is not None and not user.is_anonymous:
        album.users.add(user)

    return album
