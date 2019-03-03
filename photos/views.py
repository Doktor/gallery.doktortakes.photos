from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_GET

from core.context_processors import metadata as m
from photos.api.photo import get_photo
from photos.models import Album, Panorama, Photo, Tag
from photos.models.photo import get_exif
from photos.settings import (
    INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE, TAGLINES)

import datetime
import mimetypes
import random
import pytz
from typing import List, Callable

metadata = m(None)

FEATURED_QUERY = "?order=taken&direction=new&rating=4&rating=5"
ALBUM_QUERY = Q(parent__isnull=True, hidden=False)
ALBUM_QUERY_ADMIN = Q(parent__isnull=True)


# Helper functions


def staff_only(f: Callable) -> Callable:
    return user_passes_test(lambda u: u.is_staff)(f)


def get_albums_from_path(path: str) -> List[Album]:
    """Returns a list of Albums extracted from the given path."""
    path = path.split('/')

    if len(path) == 1:
        return [get_object_or_404(Album, slug=path[0], parent=None)]

    albums = list()
    parent = None
    for item in path:
        album = get_object_or_404(Album, slug=item, parent=parent)
        albums.append(album)
        parent = album

    return albums


def get_album_by_path(path: str) -> Album:
    """Returns the Album corresponding to the given path."""
    return get_albums_from_path(path)[-1]


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
    query = ALBUM_QUERY_ADMIN if request.user.is_staff else ALBUM_QUERY

    albums = Album.objects.filter(query).order_by('-start')

    context = {
        'tagline': random.choice(TAGLINES),
        'albums': albums[:INDEX_ALBUMS],
        'more_albums': len(albums) > INDEX_ALBUMS,
    }

    return render(request, 'index.html', context)


@require_GET
def featured(request: HttpRequest) -> HttpResponse:
    """Renders the featured photos page."""
    query = Q(album__hidden=False, rating__gte=4, sidecar_exists=True)
    photos = Photo.objects.filter(query).order_by('-taken')

    context = {
        'featured_url': reverse('search') + FEATURED_QUERY,
        'featured': photos[:INDEX_FEATURED_PHOTOS],
        'more_photos': len(photos) > INDEX_FEATURED_PHOTOS,
    }

    return render(request, 'featured.html', context)


# Albums


@require_GET
def view_albums(request: HttpRequest) -> HttpResponse:
    query = ALBUM_QUERY_ADMIN if request.user.is_staff else ALBUM_QUERY
    albums = Album.objects.filter(query).order_by('-start')

    context = {
        'albums': albums,
        'items_per_page': ITEMS_PER_PAGE,
    }

    view = request.GET.get('view', '')

    if view == 'simple':
        template = 'albums_simple.html'
    elif view == 'cards':
        template = 'albums_cards.html'
    elif view == 'details':
        template = 'albums_detailed_cards.html'
    else:
        template = 'albums_cards.html'

    return render(request, template, context)


@require_GET
def view_album(request: HttpRequest, path: str) -> HttpResponse:
    album = get_album_by_path(path)
    access, status = album.check_access(request)

    if not access:
        raise Http404

    if status is not None:
        messages.warning(request, status.message)

    photos = Photo.objects.filter(album=album, sidecar_exists=True)

    context = {
        'path': get_albums_from_path(path),
        'album': album,
        'password': 'password' in request.GET,
        'photos': photos,
        'count': photos.count(),
        'a_count': album.children.count(),
        'page_title': f"{album.name} | {metadata['TITLE']}",
        'items_per_page': ITEMS_PER_PAGE,
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'album.html', context)


# Tags


@require_GET
def view_tags(request: HttpRequest) -> HttpResponse:
    context = {'tags': Tag.objects.all()}
    return render(request, 'tags.html', context)


@require_GET
def view_tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)

    albums = tag.albums.all()
    cover = random.choice(albums).cover if albums else None

    context = {
        'tag': tag,
        'albums': albums,
        'cover': cover,
        'page_title': f"Tag: #{tag.slug} | {metadata['TITLE']}",
        'count': albums.count(),
    }

    return render(request, 'tag.html', context)


# Edit albums


@require_GET
@staff_only
def new_album(request: HttpRequest) -> HttpResponse:
    context = {
        'album': None,
        'parent': request.GET.get('parent', None)
    }

    return render(request, "new_album.html", context)


@require_GET
@staff_only
def edit_album(request: HttpRequest, path: str) -> HttpResponse:
    path = get_albums_from_path(path)
    album = path[-1]

    context = {
        'album': album,
        'photos': album.photos.all(),
        'parents': path[:-1],
        'photos_per_page': ITEMS_PER_PAGE,

        'albums': Album.objects.all().order_by('-start'),
        'items_per_page': 6,
    }

    return render(request, "edit_album.html", context)


@require_GET
@staff_only
def edit_albums(request: HttpRequest) -> HttpResponse:
    context = {
        'albums': Album.objects.all().order_by('-start'),
        'items_per_page': ITEMS_PER_PAGE
    }

    return render(request, "edit_albums.html", context)


# Photos


@require_GET
def view_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo(request, md5, validate_path=path)

    path = get_albums_from_path(path)
    album = path[-1]
    title = f"{photo.short_md5} | {photo.album.name} | {metadata['TITLE']}"

    context = {
        'path': path,
        'album': album,
        'password': 'password' in request.GET,
        'photo': photo,
        'count': album.photos.filter(sidecar_exists=True).count(),
        'exif': get_exif(photo),
        'short_md5': photo.short_md5,
        'page_title': title,
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'photo.html', context)


@require_GET
def download_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo(request, md5, validate_path=path)
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

    q = Q(album__hidden=False, sidecar_exists=True, taken__gte=start)

    photos = Photo.objects.filter(q).order_by('?')[:60]
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

    if user.is_staff:
        query = Q(parent__isnull=True, hidden=True)
    else:
        sub_query = Q(users=user)
        for group in user.groups.all():
            sub_query |= Q(groups=group)

        query = Q(parent__isnull=True) & sub_query

    albums = Album.objects.filter(query).distinct().order_by('-start')

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


# Panoramas


@require_GET
def panorama_list(request: HttpRequest) -> HttpResponse:
    p = Panorama.objects.all().order_by('-taken')
    return render(request, "panoramas.html", {'panoramas': p})


@require_GET
def panorama(request: HttpRequest, slug: str) -> HttpResponse:
    p = get_object_or_404(Panorama, slug=slug)
    return render(request, "panorama.html", {'p': p})


# Other


def view_activity(request: HttpRequest) -> HttpResponse:
    if (request.user.is_staff and not request.GET.get('cache', '')) or (
            not request.user.is_staff):

        activity = cache.get('activity')

        if activity is not None:
            return render(request, "activity.html", {'activity': activity})

    activity = {}

    album_q = Q(album__hidden=False, album__isnull=False)

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
