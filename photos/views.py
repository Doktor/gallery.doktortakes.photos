from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Count, Q
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_GET

from core.context_processors import metadata as m
from photos.models import Album, Photo, Tag
from photos.models.album import Allow
from photos.settings import (
    GIT_STATUS, INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE, TAGLINES)
from photos.utils import get_album, get_albums_for_user, get_photo

import datetime
import mimetypes
import random
import pytz
from collections import OrderedDict
from typing import Callable

metadata = m(None)

FEATURED_QUERY = "?order=taken&direction=new&rating=4&rating=5"


# Helper functions


def staff_only(f: Callable) -> Callable:
    return user_passes_test(lambda u: u.is_staff)(f)


# Error handlers


def handler_404(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    context = {'name': "404 Not Found"}
    response = render(request, 'errors/404.html', context)
    response.status_code = 404
    return response


def handler_500(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    context = {'name': "500 Internal Server Error"}
    response = render(request, 'errors/500.html', context)
    response.status_code = 500
    return response


# Debug


@require_GET
@staff_only
def debug_404(request: HttpRequest) -> HttpResponse:
    return handler_404(request)


@require_GET
@staff_only
def debug_500(request: HttpRequest) -> HttpResponse:
    return handler_500(request)


# Main pages


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    """Renders the index page."""
    all_albums = get_albums_for_user(request.user).select_related('cover')

    count = len(all_albums)
    albums = all_albums[:INDEX_ALBUMS]

    context = {
        'tagline': random.choice(TAGLINES),
        'albums': albums,
        'more_albums': count > INDEX_ALBUMS,
    }

    return render(request, 'index.html', context)


@require_GET
def featured(request: HttpRequest) -> HttpResponse:
    """Renders the featured photos page."""
    query = Q(album__access_level=Allow.PUBLIC, rating__gte=4, sidecar_exists=True)
    photos = Photo.objects.filter(query).order_by('-taken').select_related('album')

    context = {
        'featured_url': reverse('search') + FEATURED_QUERY,
        'featured': photos[:INDEX_FEATURED_PHOTOS],
        'more_photos': len(photos) > INDEX_FEATURED_PHOTOS,
    }

    return render(request, 'featured.html', context)


# Albums


@require_GET
def view_albums(request: HttpRequest) -> HttpResponse:
    return render(request, "albums.html", {})


def get_top_level_albums(user):
    return get_albums_for_user(user).order_by('-start').select_related('cover')


def get_all_albums(user, select_cover=True):
    """Returns all albums as a hierarchical list."""

    albums = (
        get_albums_for_user(user, include_children=True)
            .select_related('parent')
            .prefetch_related('children')
            .annotate(photos_count=Count('photos'))
            .order_by('-start')
    )

    if select_cover:
        albums = albums.select_related('cover')

    albums_by_pk = OrderedDict([(album.pk, album) for album in albums])

    def get(pk: int) -> tuple:
        album = albums_by_pk[pk]

        if album.children.exists():
            children = [get(child.pk) for child in album.children.all()]
        else:
            children = []

        album.total_count = (album.photos_count +
            sum(child.photos_count for child, _ in children))

        return album, children

    ret = []

    for album in albums:
        if album.parent is None:
            ret.append(get(album.pk))

    return ret


@require_GET
def view_album(request: HttpRequest, path: str) -> HttpResponse:
    album = get_album(path)

    context = {
        'album': album,
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'album.html', context)


# Tags


@require_GET
def view_tags(request: HttpRequest) -> HttpResponse:
    return render(request, 'tags.html', {})


@require_GET
def view_tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)

    context = {
        'page_title': f"Tag: #{tag.slug} | {metadata['TITLE']}",
    }

    return render(request, 'tag.html', context)


# Editor


@require_GET
@staff_only
def editor(request: HttpRequest, path=None) -> HttpResponse:
    return render(request, "editor.html", {})


# Photos


@require_GET
def view_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo(md5, request, path=path, select_album=True)

    context = {
        'allow_public': photo.album.allow_public,
        'photo': photo,
        'page_title': f"{photo.short_md5} | {photo.album.name} | {metadata['TITLE']}",
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'photo.html', context)


@require_GET
def download_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo(md5, request, path=path)
    photo.image.open()

    filename = photo.filename
    mime = mimetypes.guess_type(photo.image.url)
    response = HttpResponse(photo.image.file, content_type=mime)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response


@require_GET
def search_photos(request: HttpRequest) -> HttpResponse:
    context = {'items_per_page': ITEMS_PER_PAGE}
    return render(request, "search.html", context)


@require_GET
@staff_only
def wall(request: HttpRequest) -> HttpResponse:
    today = datetime.date.today()
    start = today - datetime.timedelta(days=365 * 2)

    q = Q(album__access_level=Allow.PUBLIC, sidecar_exists=True, taken__gte=start)

    photos = Photo.objects.filter(q).order_by('?').select_related('album')[:60]
    context = {'photos': photos}

    return render(request, 'wall.html', context)


# Users


@require_GET
@login_required
def view_users(request: HttpRequest) -> HttpResponse:
    return redirect(reverse('user', kwargs={'slug': request.user.username}))


@require_GET
@login_required
def view_user(request: HttpRequest, slug: str) -> HttpResponse:
    if request.user.username == slug:
        user = request.user
    else:
        if request.user.is_staff:
            user = get_object_or_404(User, username=slug)
        else:
            raise Http404

    albums = get_albums_for_user(user, exclude_public=True).select_related('cover')

    context = {
        'user': user,
        'albums': albums,
        'items_per_page': ITEMS_PER_PAGE,
    }

    return render(request, "user.html", context)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        user = request.user

        if user.username != slug:
            raise Http404

        return render(request, "user_password.html", {})

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        user = request.user

        if user.username != slug:
            raise Http404

        data = request.POST

        current, new, repeat = data.get('current', ''), data.get('new', ''), data.get('repeat', '')

        if not current:
            messages.error(request, "Please enter your current password.")
            return self.get(request, slug)

        if not user.check_password(current):
            messages.error(request, "The current password is incorrect.")
            return self.get(request, slug)

        if not new or not repeat:
            messages.error(request, "Please enter the new password twice.")
            return self.get(request, slug)

        if new != repeat:
            messages.error(request, "The new passwords don't match.")
            return self.get(request, slug)

        user.set_password(new)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Your password was changed successfully.", extra_tags='fade')
        return redirect(reverse('user', kwargs={'slug': user.username}))


# Other


def view_activity(request: HttpRequest) -> HttpResponse:
    if (request.user.is_staff and not request.GET.get('cache', '')) or (
            not request.user.is_staff):

        activity = cache.get('activity')

        if activity is not None:
            return render(request, "activity.html", {'activity': activity})

    activity = {}

    album_q = Q(album__access_level=Allow.PUBLIC, album__isnull=False)

    now = datetime.datetime.now().replace(tzinfo=pytz.utc)
    oldest = now - datetime.timedelta(days=180)

    photo = (
        Photo.objects
            .filter(album_q)
            .filter(uploaded__gt=oldest)
            .order_by('-uploaded')
            .values('album_id', 'uploaded'))[0]

    while photo:
        if len(activity.keys()) > 20:
            break

        album_id = photo['album_id']
        uploaded = photo['uploaded']

        # Find photos uploaded up to 1 hour before this one
        activity_group = list(
            Photo.objects
                .filter(
                    album=album_id,
                    uploaded__gt=uploaded - datetime.timedelta(hours=1),
                    uploaded__lt=uploaded)
                .order_by('uploaded')
                .values('id', 'uploaded'))

        count = len(activity_group)
        earliest = activity_group[0]['uploaded']

        sample = random.sample(activity_group, min(count, 5))
        pks = [photo['id'] for photo in sample]
        thumbs = Photo.objects.filter(id__in=pks)

        activity[earliest] = {
            'count': count,
            'album': Album.objects.get(id=album_id),
            'photos': thumbs,
        }

        photo = (
            Photo.objects
                .filter(album_q)
                .filter(uploaded__lt=earliest)
                .order_by('-uploaded')
                .values('album_id', 'uploaded'))[0]

    cache.set('activity', activity, timeout=None)

    return render(request, "activity.html", {'activity': activity})


def view_changes(request: HttpRequest) -> HttpResponse:
    return render(request, "changes.html", {'status': GIT_STATUS})
