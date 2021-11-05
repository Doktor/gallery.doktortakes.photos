from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, register_converter

from photos import views
from photos.api.urls import api_patterns
from photos.converters import MD5HashConverter

import debug_toolbar

handler404 = 'photos.views.handler_404'
handler500 = 'photos.views.handler_500'

register_converter(MD5HashConverter, 'md5')

album_patterns = [
    path('', views.view_albums, name='albums'),

    path('<path:path>/<md5:md5>/download/', views.download_photo, name='download'),
    path('<path:path>/<md5:md5>/', views.view_photo, name='photo'),
    path('<path:path>/', views.view_album, name='album'),
]

tag_patterns = [
    path('', views.view_tags, name='tags'),
    path('<slug:slug>/', views.view_tag, name='tag'),
]

urlpatterns = [
    path('log-in/', views.log_in, name='log_in'),
    path('log-out/', views.log_out, name='log_out'),

    path('', views.index, name='index'),
    path('404/', views.debug_404, name='debug_404'),
    path('500/', views.debug_500, name='debug_500'),
    path('about/', views.view_about, name='about'),
    path('admin/', admin.site.urls),
    path('albums/', include(album_patterns)),
    path('api/', include(api_patterns)),
    path('copyright/', views.view_copyright, name='copyright'),
    re_path(r'^editor/', views.editor_entry_point, name='editor'),
    path('featured/', views.featured, name='featured'),
    path('groups/', views.groups_entry_point, name='groups'),
    path('recent/', views.view_recent, name='recent'),
    path('search/', views.search_photos, name='search'),
    path('tags/', include(tag_patterns)),
    re_path(r'^users/', views.users_entry_point, name='users'),
    path('wall/', views.wall, name='wall'),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
