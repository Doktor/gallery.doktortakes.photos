from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.http import require_GET

from photos.context_processors import metadata as m
from photos.models import Photo, Tag
from photos.models.album import Allow
from photos.utils import get_album, get_photo_for_user_or_404

import datetime
import mimetypes
from typing import Callable, List


# Metadata

metadata = m(None)


class Meta:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class MetaProperty(Meta):
    def __str__(self):
        return f'  <meta property="{self.key}" content="{self.value}">'


class MetaName(Meta):
    def __str__(self):
        return f'  <meta name="{self.key}" content="{self.value}">'


def meta_to_string(items: List[Meta]) -> str:
    return '\n'.join([str(item) for item in items])


def get_canonical_url(relative_url: str) -> str:
    return f"{metadata['BASE_URL']}{relative_url}"


meta_open_graph_common = [
    MetaProperty('og:site_name', metadata['TITLE']),
    MetaProperty('og:description', metadata['DESCRIPTION']),
]

meta_open_graph_profile = [
    MetaProperty('og:type', 'profile'),
    MetaProperty('profile:first_name', 'Doktor'),
    MetaProperty('profile:username', 'Doktor'),
]

meta_open_graph_generic_image = [
    MetaProperty('og:image', f"{metadata['BASE_URL']}{static('images/camera.png')}"),
    MetaProperty('og:image:type', 'image/png'),
    MetaProperty('og:image:width', '500'),
    MetaProperty('og:image:height', '500'),
]

def meta_open_graph_article(last_update=metadata['LAST_UPDATE']):
    return [
        MetaProperty('og:type', 'article'),
        MetaProperty('article:author', metadata['NAME']),
        MetaProperty('article:published_time', last_update.isoformat()),
        MetaProperty('article:modified_time', last_update.isoformat()),
    ]

meta_twitter_common = [
    MetaName('twitter:site', metadata['TWITTER']),
    MetaName('twitter:creator', metadata['TWITTER']),
    MetaName('twitter:description', metadata['DESCRIPTION']),
]

meta_no_robots = MetaName('robots', 'noindex, nofollow')


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
    context = {
        'title': 'Index',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('index'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_article(),
        ])
    }

    return render(request, 'base.html', context)


@require_GET
def view_copyright(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Copyright',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('copyright'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_article(),
        ]),
    }

    return render(request, 'base.html', context)


@require_GET
def view_about(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'About',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('about'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_profile,
        ]),
    }

    return render(request, 'base.html', context)


# Albums


@require_GET
def view_albums(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Albums',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('albums'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_article(),
        ]),
    }

    return render(request, 'base.html', context)


@require_GET
def view_album(request: HttpRequest, path: str) -> HttpResponse:
    album = get_album(path)

    # If the album doesn't exist or the album isn't public, don't render meta tags
    if album is None or album.access_level > Allow.PUBLIC:
        return view_restricted_album(request)

    title = f"{album.name} | {metadata['TITLE']}"
    base_url = metadata['BASE_URL'] if settings.LOCAL_STORAGE else ''
    cover_url = f"{base_url}{album.cover.image.url}"

    meta = [
        *meta_open_graph_common,
        MetaProperty('og:title', title),
        MetaProperty('og:url', get_canonical_url(album.get_absolute_url())),
        MetaProperty('og:updated_time', album.start.isoformat()),

        *meta_open_graph_article(last_update=album.start),
    ]

    if album.cover is not None:
        meta.extend([
            MetaProperty('og:image', cover_url),
            MetaProperty('og:image:type', 'image/jpeg'),
            MetaProperty('og:image:width', album.cover.width),
            MetaProperty('og:image:height', album.cover.height),
        ])
    else:
        meta.extend(meta_open_graph_generic_image)

    meta.extend([
        *meta_twitter_common,
        MetaName('twitter:card', 'photo'),
        MetaName('twitter:title', title),
    ])

    if album.cover is not None:
        meta.append(MetaProperty('twitter:image', cover_url))

    if album.access_level > Allow.PUBLIC:
        meta.append(meta_no_robots)

    context = {
        'title': album.name,
        'meta': meta_to_string(meta)
    }

    return render(request, 'base.html', context)


@require_GET
def view_restricted_album(request: HttpRequest) -> HttpResponse:
    return render(request, 'base.html', {})


# Tags


@require_GET
def view_tags(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Tags',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('tags'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_article(),
        ])
    }

    return render(request, 'base.html', context)


@require_GET
def view_tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)

    title = f'Tag: #{tag.slug}'
    context = {
        'title': title,
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', title),
            MetaProperty('og:url', get_canonical_url(tag.get_absolute_url())),

            *meta_open_graph_article(),

            *meta_twitter_common,
            MetaName('twitter:card', 'photo'),
            MetaName('twitter:title', title),
        ]),
    }

    return render(request, 'base.html', context)


# Editor


@require_GET
def editor_entry_point(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Editor',
        'meta': meta_to_string([
            meta_no_robots,
        ])
    }
    return render(request, 'base.html', context)


# Photos


@require_GET
def view_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo_for_user_or_404(request, md5, path=path, select_album=True)

    title = f"{photo.short_md5} | {photo.album.name}"
    full_title = f"{title} | {metadata['TITLE']}"

    meta = [
        *meta_open_graph_common,
        MetaProperty('og:title', full_title),
        MetaProperty('og:url', get_canonical_url(photo.get_absolute_url())),
        MetaProperty('og:updated_time', photo.taken.isoformat()),

        *meta_open_graph_article(last_update=photo.taken),

        MetaProperty('og:image', get_canonical_url(photo.image.url)),
        MetaProperty('og:image:type', 'image/jpeg'),
        MetaProperty('og:image:width', photo.width),
        MetaProperty('og:image:height', photo.height),

        *meta_twitter_common,
        MetaName('twitter:card', 'photo'),
        MetaName('twitter:title', full_title),
        MetaName('twitter:image', get_canonical_url(photo.image.url)),
    ]

    if photo.access_level > Allow.PUBLIC:
        meta.append(meta_no_robots)

    context = {
        'title': title,
        'meta': meta_to_string(meta),
    }

    return render(request, 'base.html', context)


@require_GET
def download_photo(request: HttpRequest, path: str, md5: str) -> HttpResponse:
    photo = get_photo_for_user_or_404(request, md5, path=path)
    photo.image.open()

    filename = photo.filename
    mime = mimetypes.guess_type(photo.image.url)
    response = HttpResponse(photo.image.file, content_type=mime)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response


@require_GET
def search_photos(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Search',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('search'))),
            *meta_open_graph_generic_image,

            *meta_open_graph_article(),
        ])
    }
    return render(request, 'base.html', context)



@require_GET
def wall(request: HttpRequest) -> HttpResponse:
    today = datetime.date.today()
    start = today - datetime.timedelta(days=365 * 2)

    q = Q(album__access_level=Allow.PUBLIC, sidecar_exists=True, taken__gte=start)

    photos = Photo.objects.filter(q).order_by('?').select_related('album')[:60]
    context = {'photos': photos}

    return render(request, 'wall.html', context)


# Groups


@require_GET
def groups_entry_point(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Groups',
        'meta': meta_to_string([
            meta_no_robots,
        ])
    }

    return render(request, 'base.html', context)


# Users

@require_GET
def log_in(request: HttpRequest) -> HttpResponse:
    context = {
        'title': "Log in",
    }

    return render(request, "base.html", context)


@require_GET
def log_out(request: HttpRequest) -> HttpResponse:
    context = {
        'title': "Log out",
    }

    return render(request, "base.html", context)


@require_GET
def users_entry_point(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Users',
        'meta': meta_to_string([
            meta_no_robots,
        ])
    }

    return render(request, 'base.html', context)


# Other


def view_recent(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Recent',
        'meta': meta_to_string([
            *meta_open_graph_common,
            MetaProperty('og:title', metadata['TITLE']),
            MetaProperty('og:url', get_canonical_url(reverse('recent'))),

            *meta_open_graph_article(),
        ]),
    }

    return render(request, 'base.html', context)
