from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, register_converter

from photos.converters import MD5HashConverter
register_converter(MD5HashConverter, 'md5')

from photos import views
from photos.api.urls import api_patterns

import debug_toolbar

handler404 = 'photos.views.handler_404'
handler500 = 'photos.views.handler_500'


album_patterns = [
    path('', views.view_albums, name='albums'),

    path('<path:path>/<md5:md5>', views.view_photo, name='photo'),
    path('<path:path>/', views.view_album, name='album'),
]

redirect_patterns = [
    path('admin/photos/<md5:md5>', views.redirect_admin_photo),
]

featured_patterns = [
    path('', views.view_featured, name='featured'),
    path('<path:path>/', views.view_featured_album, name='featured_album'),
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
    path('admin/', admin.site.urls),
    path('albums/', include(album_patterns)),
    path('api/', include(api_patterns)),
    path('about/', views.view_about, name='about'),
    path('copyright/', views.view_copyright, name='copyright'),
    path('featured/', include(featured_patterns)),
    re_path(r'^debug/', views.index, name='debug'),
    path('groups/', views.groups_entry_point, name='groups'),
    re_path(r'^manage/', views.editor_entry_point, name='editor'),
    path('redirect/', include(redirect_patterns)),
    path('search/', views.search_photos, name='search'),
    path('tags/', include(tag_patterns)),
    re_path(r'^taxa/', views.index),
    re_path(r'^users/', views.users_entry_point, name='users'),
    path('wall/', views.wall, name='wall'),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
