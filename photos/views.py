from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from photos.context_processors import metadata as m
from photos.forms import AlbumForm
from photos.models import Album, Photo
from photos.settings import (
    INDEX_ALBUMS, INDEX_FEATURED_PHOTOS, ITEMS_PER_PAGE, TAGLINES)

import mimetypes
import random

metadata = m(None)


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
    path = path.split('/')

    if len(path) == 1:
        return get_object_or_404(Album, slug=path[0], parent=None)

    previous = None
    for item in path:
        a = get_object_or_404(Album, slug=item, parent=previous)
        previous = a

    return a


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


def index(request):
    """Renders the index page."""
    albums = Album.objects.filter(parent__isnull=True).order_by('-start')
    featured = Photo.objects.filter(rating__gte=4).order_by('-taken')

    context = {
        'tagline': random.choice(TAGLINES),
        'featured': featured[:INDEX_FEATURED_PHOTOS],
        'more_photos': len(featured) > INDEX_FEATURED_PHOTOS,
        'albums': albums[:INDEX_ALBUMS],
        'more_albums': len(albums) > INDEX_ALBUMS,
    }

    return render(request, 'index.html', context)


def photos_list(request):
    """Renders the list of albums."""
    albums = Album.objects.filter(parent__isnull=True).order_by('-start')
    context = {'albums': albums}
    return render(request, 'photos.html', context)


def search_photos(request):
    context = {
        'items_per_page': ITEMS_PER_PAGE
    }
    return render(request, "search.html", context)


@require_http_methods(['GET'])
def album(request, path):
    """Renders album pages."""
    a = get_album_by_path(path)
    title = f"{a.name} | {metadata['TITLE']}"

    context = {
        'path': get_albums_from_path(path),
        'album': a,
        'page_title': title,
        'items_per_page': ITEMS_PER_PAGE,
    }
    return render(request, 'album.html', context)


@require_http_methods(['POST'])
@login_required
def delete_album(request, path):
    """Deletes an album."""
    a = get_album_by_path(path)

    name = request.POST.get('name')
    if name != a.name:
        messages.error(request, "Incorrect name specified.")
        return redirect('edit_album', path=a.get_path())

    a.delete()
    messages.success(request, "Album \"%s\" deleted successfully." % name)
    return redirect('edit')


@login_required
def edit_album(request, path):
    """Renders the edit album page."""

    if request.method == 'GET':
        a = get_album_by_path(path)
        form = AlbumForm(instance=a)

        context = {
            'album': a,
            'parents': get_albums_from_path(path)[:-1],
            'form': form,
        }

        return render(request, "edit_album.html", context)

    elif request.method == 'POST':
        a = get_album_by_path(path)

        form = AlbumForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            messages.success(request, "Album updated successfully.")
            return redirect('edit_album', path=a.get_path())


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

    # Delete a photo
    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return JsonResponse({'success': False})
        try:
            if not (path and md5):
                raise ValueError('Photo incorrectly specified')

            a = get_album_by_path(path)
            p = Photo.objects.get(album=a, md5=md5)

            p.thumbnail.delete(save=False)
            p.image.delete(save=False)
            p.delete()

            success = True

        except (IOError, OSError) as e:
            # TODO send email
            success = False

        except ValueError:
            success = False

        except Photo.DoesNotExist:
            success = False

        finally:
            return JsonResponse({'success': success})


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
        p.image.save(file.name, File(file))
        p.save()

    return JsonResponse({'success': True})


def site_login(request):
    """Log in to the site."""
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "Logged in successfully.")
            return redirect(next_url)
        else:
            # TODO: next parameter is not preserved
            messages.error(request, "Invalid username or password.")
            return redirect(
                "{url}?next={next}".format(url=reverse('login'), next=next_url))

    return render(request, "login.html", dict())


@login_required
def site_logout(request):
    """Log out of the site."""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect(reverse('index'))


def commissions(request):
    return redirect(
        "https://docs.google.com/document/d/"
        "1iWG2WM-nicocfP_vT6-VF8KO-EPla8-AARo5x7rZXIs/", permanent=False)
