from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from core.context_processors import metadata as m
from photos.models import Album, Photo, Tag
from photos.models.album import Allow
from photos.settings import (
    GIT_STATUS, INDEX_ALBUMS, ITEMS_PER_PAGE, TAGLINES)
from photos.utils import get_album, get_albums_for_user, get_photo

import datetime
import mimetypes
import random
import pytz
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
    return render(request, 'featured.html', {})


# Albums


@require_GET
def view_albums(request: HttpRequest) -> HttpResponse:
    return render(request, "albums.html", {})


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
    return render(request, "search.html", {})


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


@require_GET
@login_required
def change_password(request: HttpRequest, slug: str) -> HttpResponse:
    user = request.user

    if user.username != slug:
        raise Http404

    return render(request, "user_password.html", {})


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
