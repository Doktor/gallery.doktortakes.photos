import factory
from enum import Enum
from typing import Union

from django.contrib.auth.models import User, AnonymousUser

from photos.models import Album
from photos.models.album import Allow


DjangoUser = Union[AnonymousUser, User]


class Level(Enum):
    ANONYMOUS = "anonymous"
    USER = "user"
    OWNER = "owner"
    STAFF = "staff"
    SUPERUSER = "superuser"


# Factory classes


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user-{n}")
    password = factory.Faker('password', length=8, digits=True, lower_case=True)

    is_staff = False

    class Meta:
        model = User


class AlbumFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Album {n} Title")
    start = factory.Faker('date')

    class Meta:
        model = Album


# Factory functions


def create_user(level: Level) -> DjangoUser:
    if level == Level.ANONYMOUS:
        return AnonymousUser()
    elif level == Level.USER:
        return UserFactory()
    elif level == Level.OWNER:
        return UserFactory()
    elif level == Level.STAFF:
        return UserFactory(is_staff=True)
    elif level == Level.SUPERUSER:
        return UserFactory(is_staff=True, is_superuser=True)


def create_album(access_level: Allow, user: DjangoUser = None):
    album = AlbumFactory(access_level=access_level)

    if user is not None and not user.is_anonymous:
        album.users.add(user)

    return album
