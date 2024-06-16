import factory
from enum import Enum
from typing import Union

from django.contrib.auth.models import User, AnonymousUser

from photos.models import License

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


class LicenseFactory(factory.DjangoModelFactory):
    class Meta:
        model = License


# Factory functions


def create_anonymous_user():
    return create_user(Level.ANONYMOUS)


def create_standard_user():
    return create_user(Level.USER)


def create_superuser():
    return create_user(Level.SUPERUSER)


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
