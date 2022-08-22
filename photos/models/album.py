from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.http import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework.request import Request

from photos.context_processors import metadata

from typing import List, Union

m = metadata(None)

SIZE_2400 = '2400'
SIZE_3000 = '3000'
SIZE_3600 = '3600'
SIZE_3840 = '3840'
SIZE_4800 = '4800'
SIZE_6000 = '6000'

DISPLAY_IMAGE_SIZES = (
    (SIZE_2400, '2400 x 1600'),
    (SIZE_3000, '3000 x 2000'),
    (SIZE_3600, '3600 x 2400'),
    (SIZE_3840, '3840 x 2560'),
    (SIZE_4800, '4800 x 3200'),
    (SIZE_6000, '6000 x 4000'),
)


class Allow:
    PUBLIC = 0
    SIGNED_IN = 10
    OWNERS = 20
    STAFF = 30
    SUPERUSER = 100


ACCESS_LEVELS = (
    (Allow.PUBLIC, "Public"),
    (Allow.SIGNED_IN, "Signed in"),
    (Allow.OWNERS, "Owners"),
    (Allow.STAFF, "Staff"),
    (Allow.SUPERUSER, "Superusers"),
)


class Album(MPTTModel):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)

    place = models.CharField(
        max_length=128, blank=True,
        help_text="The specific venue, building, or place")
    location = models.CharField(
        max_length=128, blank=True,
        help_text="The city, state, and country")
    timezone = models.CharField(max_length=100, default='US/Eastern')
    description = models.CharField(
        max_length=1000, blank=True,
        help_text="A brief description of this album")

    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)

    display_image_size = models.CharField(
        max_length=4, choices=DISPLAY_IMAGE_SIZES, default=SIZE_3840)

    cover = models.OneToOneField(
        'Photo', models.SET_NULL,
        related_name='cover_for', blank=True, null=True,
        help_text="The cover photo for this album")

    parent = TreeForeignKey(
        'self', models.SET_NULL,
        related_name='children', blank=True, null=True,
        help_text="The album that contains this album")

    path = models.TextField(
        blank=True, editable=False,
        help_text="The path to this album; automatically set")

    # Permissions
    access_level = models.PositiveSmallIntegerField(
        choices=ACCESS_LEVELS, default=Allow.PUBLIC)

    access_code = models.CharField(max_length=128, blank=True)
    users = models.ManyToManyField(User, related_name='albums', blank=True)
    groups = models.ManyToManyField(Group, related_name='albums', blank=True)

    tags = models.ManyToManyField('Tag', related_name='albums', blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def allow_public(self) -> bool:
        return self.access_level == Allow.PUBLIC

    def clean(self) -> None:
        self.validate_fields(model_to_dict(self))

    @property
    def count(self) -> int:
        """Returns the number of photos in this album and all child albums."""
        return (self.photos.count() +
                sum([album.count for album in self.children.all()]))

    def check_access(self, request: Union[HttpRequest, Request]) -> bool:
        album = self
        user = request.user

        try:
            code = request.GET['code']
        except KeyError:
            code = False

        # Access code supersedes all other permission checks
        if album.access_code and code and album.access_code == code:
            return True

        if album.access_level == Allow.SUPERUSER:
            return user.is_superuser

        elif album.access_level == Allow.STAFF:
            return user.is_staff

        elif album.access_level == Allow.OWNERS:
            if user in album.users.all():
                return True
            elif any(group in user.groups.all() for group in album.groups.all()):
                return True
            else:
                return user.is_staff

        elif album.access_level == Allow.SIGNED_IN:
            return user.is_authenticated

        elif album.access_level == Allow.PUBLIC:
            return True

        return False

    def delete(self, using=None, keep_parents=False) -> None:
        for photo in self.photos.all():
            photo.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self) -> str:
        return reverse('album', args=[self.path])

    def get_access_code_query(self, separator: bool = False) -> str:
        if self.access_code:
            q = f"?code={self.access_code}"

            if separator:
                return q + '&'
            return q
        else:
            return ''

    def get_access_code_url(self) -> str:
        return self.get_absolute_url() + self.get_access_code_query()

    def get_admin_url(self) -> str:
        return reverse('admin:photos_album_change', args=[self.pk])

    def get_all_subalbums(self, include_self: bool = False) -> List['Album']:
        albums = []

        if include_self:
            albums.append(self)

        for album in self.children.all():
            albums += album.get_all_subalbums(include_self=True)

        return albums

    def get_all_subphotos(self, include_self: bool = False) -> List['Photo']:
        photos = []

        if include_self:
            photos += list(self.photos.all())

        for album in self.children.all():
            photos += album.get_all_subphotos(include_self=True)

        return photos

    def get_full_date(self) -> str:
        template = "{date:%a} {date.year}-{date.month:02}-{date.day:02}"

        if not self.end or self.start == self.end:
            full_date = template.format(date=self.start)
        else:
            full_date = "{start} &ndash; {end}".format(
                start=template.format(date=self.start),
                end=template.format(date=self.end))

        return mark_safe(full_date)

    def get_full_location(self) -> str:
        place = self.get_place()
        location = self.get_location()

        if place and location:
            return f"{place}, {location}"

        return place or location or ""

    def get_groups(self) -> str:
        return ', '.join(f'Group: {group.name}' for group in self.groups.all())

    def get_location(self) -> str:
        if self.location or not self.parent:
            return self.location

        return self.parent.get_location()

    def get_path(self, previous='', divider='/') -> str:
        if not self.parent:
            if not previous:
                return self.slug
            else:
                return self.slug + divider + previous

        if not previous:
            return self.parent.get_path(
                previous=self.slug, divider=divider)
        else:
            return self.parent.get_path(
                previous=f"{self.slug}{divider}{previous}", divider=divider)

    def get_place(self) -> str:
        if self.place or not self.parent:
            return self.place

        return self.parent.get_place()

    def get_users(self) -> str:
        return ', '.join(user.username.capitalize() for user in self.users.all())

    def save(self, *args, **kwargs) -> None:
        self.clean()

        self.slug = slugify(self.name)
        self.path = self.get_path()

        super().save(*args, **kwargs)

    @staticmethod
    def validate_fields(fields: dict) -> None:
        has_id = fields.get('id', None) is not None

        if isinstance(fields['parent'], Album):
            parent_id = fields['parent'].id
        else:
            parent_id = None

        if fields.get('end', None) is not None and fields['start'] > fields['end']:
            raise ValidationError('The end date should be later than the start date.')

        if has_id and fields['id'] == parent_id:
            raise ValidationError('An album can\'t be its own parent.')

        try:
            album = Album.objects.get(name=fields['name'], parent__id=parent_id)
        except Album.DoesNotExist:
            return

        if has_id and album.id == fields['id']:
            return

        if parent_id is None:
            raise ValidationError('A top-level album with that name already exists.')
        else:
            raise ValidationError('An album with that name and parent album already exists.')

    class Meta:
        get_latest_by = 'start'

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent'],
                name='unique_name'
            ),
            models.UniqueConstraint(
                fields=['name'],
                condition=Q(parent=None),
                name='unique_name_top_level',
            ),
        ]


@receiver(pre_save, sender=Album,
          dispatch_uid="photos.models.create_album_cover")
def create_album_cover(sender, instance: Album, **kwargs) -> None:
    album = instance

    try:
        prev = Album.objects.get(pk=album.pk)
    except Album.DoesNotExist:
        return
    else:
        if prev.cover == album.cover:
            return

        if album.cover is None:
            return

    from photos.tasks import update_large_square_thumbnail
    update_large_square_thumbnail(album.cover, album.cover.get_original())
    album.cover.save()
