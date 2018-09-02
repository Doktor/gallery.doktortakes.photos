from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_GET

from core.context_processors import metadata as m
from photos.forms import AlbumForm
from photos.models import Album, Panorama, Photo, Tag
from core.settings import (
    INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE, TAGLINES)

import datetime
import mimetypes
import random

metadata = m(None)

FEATURED_QUERY = "?order=taken&direction=new&rating=4&rating=5"


def get_albums_from_path(path):
    """Returns a list of Albums extracted from the given path."""
    path = path.split('/')

    if len(path) == 1:
        return [get_object_or_404(Album, slug=path[0], parent=None)]

    albums = list()
    parent = None
    for item in path:
        a = get_object_or_404(Album, slug=item, parent=parent)
        albums.append(a)
        parent = a

    return albums


def get_album_by_path(path):
    """Returns the Album corresponding to the given path."""
    return get_albums_from_path(path)[-1]


def get_photo(path, md5):
    """Returns the Photo in the album with the given path, and with the
    given MD5 hash."""
    a = get_album_by_path(path)
    p = get_object_or_404(Photo, md5=md5, album=a)
    return p


def handler404(request):
    """Renders 404 errors."""
    context = {'name': "404 Not Found"}
    response = render(request, 'errors/404.html', context)
    response.status_code = 404
    return response


def handler500(request):
    """Renders 500 errors."""
    context = {'name': "500 Internal Server Error"}
    response = render(request, 'errors/500.html', context)
    response.status_code = 500
    return response


@login_required
def debug404(request):
    """Test page for a 404 error."""
    return handler404(request)


@login_required
def debug500(request):
    """Test page for a 500 error."""
    return handler500(request)


QUERY_ADMIN = Q(parent__isnull=True)
QUERY = Q(parent__isnull=True, hidden=False)


def index(request):
    """Renders the index page."""
    query = QUERY_ADMIN if request.user.is_superuser else QUERY

    albums = Album.objects.filter(query).order_by('-start')

    context = {
        'tagline': random.choice(TAGLINES),
        'albums': albums[:INDEX_ALBUMS],
        'more_albums': len(albums) > INDEX_ALBUMS,
    }

    return render(request, 'index.html', context)


def featured(request):
    """Renders the featured photos page."""
    q = Q(album__hidden=False, rating__gte=4)
    photos = Photo.objects.filter(q).order_by('-taken')

    context = {
        'featured_url': reverse('search') + FEATURED_QUERY,
        'featured': photos[:INDEX_FEATURED_PHOTOS],
        'more_photos': len(photos) > INDEX_FEATURED_PHOTOS,
    }

    return render(request, 'featured.html', context)


def wall(request):
    q = Q(album__hidden=False) & Q(album__password=None)

    # Only show photos taken within the last 12 months
    today = datetime.date.today()
    q = q & Q(taken__year__gte=today.year - 1, taken__month__gte=today.month)

    photos = Photo.objects.filter(q).order_by('?')[:120]
    context = {'photos': photos}

    return render(request, 'wall.html', context)


def album_list(request):
    """Renders the list of albums."""
    query = QUERY_ADMIN if request.user.is_superuser else QUERY

    albums = Album.objects.filter(query).order_by('-start')
    context = {'albums': albums}

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


def search_photos(request):
    context = {
        'items_per_page': ITEMS_PER_PAGE
    }
    return render(request, "search.html", context)


@require_http_methods(['GET'])
def album(request, path):
    """Renders album pages."""
    a = get_album_by_path(path)

    if a.password:
        password = request.GET.get('password', '')

        if password != a.password:
            if request.user.is_superuser:
                base = reverse('album', kwargs={'path': path})
                return redirect(base + f"?password={a.password}")

            raise Http404

    title = f"{a.name} | {metadata['TITLE']}"

    context = {
        'path': get_albums_from_path(path),
        'album': a,
        'count': a.photos.count(),
        'page_title': title,
        'items_per_page': ITEMS_PER_PAGE,
    }
    return render(request, 'album.html', context)


@require_GET
def tags(request):
    context = {'tags': Tag.objects.all()}
    return render(request, 'tags.html', context)


@require_GET
def tag(request, slug):
    t = get_object_or_404(Tag, slug=slug)

    albums = t.albums.all()
    cover = random.choice(albums).cover if albums else None

    title = f"Tag: #{t.slug} | {metadata['TITLE']}"

    context = {
        'tag': t,
        'albums': albums,
        'cover': cover,
        'page_title': title,
        'count': albums.count(),
    }
    return render(request, 'tag.html', context)


def panorama_list(request):
    p = Panorama.objects.all().order_by('-taken')
    return render(request, "panoramas.html", {'panoramas': p})


def panorama(request, slug):
    p = get_object_or_404(Panorama, slug=slug)
    return render(request, "panorama.html", {'p': p})


@require_GET
@login_required
def edit_album(request, path):
    """Renders the edit album page."""
    a = get_album_by_path(path)

    context = {
        'album': a,
        'photos': a.photos.all(),
        'count': a.photos.count(),
        'parents': get_albums_from_path(path)[:-1],
    }

    return render(request, "edit_album.html", context)


def photo(request, path, md5):
    """Renders photo pages."""

    if request.method == 'GET':
        from photos.api import get_exif

        path = get_albums_from_path(path)
        a = path[-1]
        p = Photo.objects.get(album=a, md5=md5)
        exif = get_exif(p)
        short_md5 = p.md5[:7]
        title = f"{short_md5} | {p.album.name} | {metadata['TITLE']}"

        context = {
            'path': path,
            'album': a,
            'photo': p,
            'exif': exif,
            'short_md5': short_md5,
            'page_title': title,
        }

        return render(request, 'photo.html', context)


def photo_download(request, path, md5):
    """Starts a download for a photo."""
    p = get_photo(path, md5)

    p.image.open()

    filename = p.filename
    mime = mimetypes.guess_type(p.image.url)
    response = HttpResponse(p.image.file, content_type=mime)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response


@login_required
def edit_content(request):
    """Renders the content editor."""
    albums = Album.objects.filter(parent__isnull=True).order_by('-start')
    context = {'albums': albums}
    return render(request, "edit.html", context)


@login_required
def new_album(request):
    """Renders the add new album page."""
    if request.method == 'POST':
        form = AlbumForm(request.POST)

        if form.is_valid():
            a = form.save()

            messages.success(request, "Album created successfully.")
            return redirect('edit_album', path=a.get_path())

    context = {'form': AlbumForm()}
    return render(request, "new_album.html", context)


@login_required
def upload_photo(request, path):
    """Upload a photo to an album."""
    if request.method != 'POST':
        raise Http404()

    files = request.FILES.getlist('files')

    for file in files:
        p = Photo()
        p.album = get_album_by_path(path)
        p.original = file
        p.save()

    return JsonResponse({'success': True})
