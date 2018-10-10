from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from core.context_processors import metadata as m
from photos.models import Album, Panorama, Photo, Tag
from photos.models.photo import get_exif
from photos.settings import (
    INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE, TAGLINES)

import datetime
import mimetypes
import random

metadata = m(None)

FEATURED_QUERY = "?order=taken&direction=new&rating=4&rating=5"
ALBUM_QUERY = Q(parent__isnull=True, hidden=False)
ALBUM_QUERY_ADMIN = Q(parent__isnull=True)


# Helper functions


def staff_only(f):
    return user_passes_test(lambda u: u.is_staff)(f)


def get_albums_from_path(path):
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


def get_album_by_path(path) -> Album:
    """Returns the Album corresponding to the given path."""
    return get_albums_from_path(path)[-1]


def get_photo(path, md5) -> Photo:
    """Returns the Photo in the album with the given path, and with the
    given MD5 hash."""
    a = get_album_by_path(path)
    p = get_object_or_404(Photo, md5=md5, album=a)
    return p


# Error handlers


def handler_404(request, exception=None):
    context = {'name': "404 Not Found"}
    response = render(request, 'errors/404.html', context)
    response.status_code = 404
    return response


def handler_500(request, exception=None):
    context = {'name': "500 Internal Server Error"}
    response = render(request, 'errors/500.html', context)
    response.status_code = 500
    return response


# Debug


@require_GET
@staff_only
def debug_404(request):
    return handler_404(request)


@require_GET
@staff_only
def debug_500(request):
    return handler_500(request)


# Main pages


@require_GET
def index(request):
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
def featured(request):
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
def view_albums(request):
    hidden = request.GET.get('hidden', '')

    if request.user.is_staff and hidden:
        query = Q(parent__isnull=True, hidden=True)
    elif hidden:
        sub_query = Q(users=request.user)
        for group in request.user.groups.all():
            sub_query |= Q(groups=group)

        query = Q(parent__isnull=True) & sub_query
    else:
        query = ALBUM_QUERY_ADMIN if request.user.is_staff else ALBUM_QUERY

    albums = Album.objects.filter(query).order_by('-start')

    context = {
        'albums': albums,
        'items_per_page': ITEMS_PER_PAGE,
        'view_hidden': bool(hidden),
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
def view_album(request, path):
    album = get_album_by_path(path)

    if not album.check_access(request):
        raise Http404

    photos = Photo.objects.filter(album=album, sidecar_exists=True)

    context = {
        'path': get_albums_from_path(path),
        'album': album,
        'password': 'password' in request.GET,
        'photos': photos,
        'count': photos.count(),
        'page_title': f"{album.name} | {metadata['TITLE']}",
        'items_per_page': ITEMS_PER_PAGE,
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'album.html', context)


# Tags


@require_GET
def view_tags(request):
    context = {'tags': Tag.objects.all()}
    return render(request, 'tags.html', context)


@require_GET
def view_tag(request, slug):
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
def new_album(request):
    context = {
        'album': None,
        'parent': request.GET.get('parent', None)
    }

    return render(request, "new_album.html", context)


@require_GET
@staff_only
def edit_album(request, path):
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
def edit_albums(request):
    context = {
        'albums': Album.objects.all().order_by('-start'),
        'items_per_page': ITEMS_PER_PAGE
    }

    return render(request, "edit_albums.html", context)


# Photos


@require_GET
def view_photo(request, path, md5):
    photo = Photo.objects.get(md5=md5)

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    path = get_albums_from_path(path)
    short_md5 = photo.md5[:7]
    title = f"{short_md5} | {photo.album.name} | {metadata['TITLE']}"

    context = {
        'path': path,
        'album': path[-1],
        'password': 'password' in request.GET,
        'photo': photo,
        'exif': get_exif(photo),
        'short_md5': short_md5,
        'page_title': title,
        'local_storage': settings.LOCAL_STORAGE,
    }

    return render(request, 'photo.html', context)


@require_GET
def download_photo(request, path, md5):
    photo = get_photo(path, md5)

    if not photo.sidecar_exists:
        raise Http404

    if not photo.check_access(request):
        raise Http404

    photo.image.open()

    filename = photo.filename
    mime = mimetypes.guess_type(photo.image.url)
    response = HttpResponse(photo.image.file, content_type=mime)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response


@require_GET
def search_photos(request):
    context = {'items_per_page': ITEMS_PER_PAGE}
    return render(request, "search.html", context)


@require_GET
@staff_only
def wall(request):
    q = Q(album__hidden=False) & Q(album__password='')

    # Only show photos taken within the last 12 months
    today = datetime.date.today()
    q = q & Q(taken__year__gte=today.year - 1, taken__month__gte=today.month)

    photos = Photo.objects.filter(q).order_by('?')[:120]
    context = {'photos': photos}

    return render(request, 'wall.html', context)


# Panoramas


@require_GET
def panorama_list(request):
    p = Panorama.objects.all().order_by('-taken')
    return render(request, "panoramas.html", {'panoramas': p})


@require_GET
def panorama(request, slug):
    p = get_object_or_404(Panorama, slug=slug)
    return render(request, "panorama.html", {'p': p})
