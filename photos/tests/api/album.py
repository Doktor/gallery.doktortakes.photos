import factory
from datetime import timedelta

from django.utils.text import slugify

from photos.models import Album


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album Name {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    path = factory.LazyAttribute(lambda o: o.slug)

    start = factory.Faker('date_object')
    end = factory.LazyAttribute(lambda o: o.start + timedelta(days=10))

    class Meta:
        model = Album
