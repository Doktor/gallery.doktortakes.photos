from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter
from django.views.generic import TemplateView

from auth.urls import url_log_in, url_log_out
from core.converters import MD5HashConverter
from photos import views
from photos.api.urls import api_patterns

import debug_toolbar

handler404 = 'photos.views.handler_404'
handler500 = 'photos.views.handler_500'

register_converter(MD5HashConverter, 'md5')

album_patterns = [
    path('', views.view_albums, name='albums'),

    path('<path:path>/', views.view_album, name='album'),
    path('<path:path>/<md5:md5>', views.view_photo, name='photo'),
    path('<path:path>/<md5:md5>/download/', views.download_photo, name='download'),
]

editor_patterns = [
    path('', views.editor, name='editor'),
    path('albums/new/', views.editor, name='editor_new_album'),
    path('albums/edit/<path:path>/', views.editor, name='editor_edit_album'),
]

tag_patterns = [
    path('', views.view_tags, name='tags'),
    path('<slug:slug>/', views.view_tag, name='tag'),
]

user_patterns = [
    path('', views.view_users, name='users'),
    path('<slug:slug>/', views.view_user, name='user'),
    path('<slug:slug>/password/', views.change_password, name='password'),
]

urlpatterns = [
    url_log_in,
    url_log_out,

    path('', views.index, name='index'),
    path('404/', views.debug_404, name='debug_404'),
    path('500/', views.debug_500, name='debug_500'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('admin/', admin.site.urls),
    path('albums/', include(album_patterns)),
    path('api/', include(api_patterns)),
    path('copyright/', TemplateView.as_view(template_name='copyright.html'), name='copyright'),
    path('editor/', include(editor_patterns)),
    path('featured/', views.featured, name='featured'),
    path('recent/', views.view_recent, name='recent'),
    path('search/', views.search_photos, name='search'),
    path('tags/', include(tag_patterns)),
    path('users/', include(user_patterns)),
    path('wall/', views.wall, name='wall'),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
