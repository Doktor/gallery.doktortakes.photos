from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter
from django.views.generic import TemplateView

from auth.urls import url_log_in, url_log_out
from core.converters import MD5HashConverter
from photos import api, views

handler404 = 'photos.views.handler404'
handler500 = 'photos.views.handler500'

register_converter(MD5HashConverter, 'md5')

album_patterns = [
    path('', views.album_list, name='albums'),

    path('new/', views.new_album, name='new_album'),
    path('edit/', views.edit_albums, name='edit_albums'),

    path('search/', views.search_photos, name='search'),

    path('<path:path>/edit/', views.edit_album, name='edit_album'),
    path('<path:path>/upload/', views.upload_photo, name='upload'),

    path('<path:path>/', views.album, name='album'),
    path('<path:path>/<md5:md5>', views.photo, name='photo'),
    path('<path:path>/<md5:md5>/download', views.download, name='download'),
]

tag_patterns = [
    path('', views.tags, name='tags'),
    path('<slug:slug>/', views.tag, name='tag'),
]

api_patterns = [
    path('photo/', api.PhotoView.as_view(), name='api_photo'),

    path('photo/previous/', api.previous_photo, name='previous_photo'),
    path('photo/next/', api.next_photo, name='next_photo'),
    path('photo/first/', api.first_photo, name='first_photo'),
    path('photo/last/', api.last_photo, name='last_photo'),

    path('album/', api.AlbumView.as_view(), name='api_album'),

    path('album/photos/', api.get_album_photos, name='get_album_photos'),

    path('search/', api.search_photos, name='search_photos'),
]

panorama_patterns = [
    path('', views.panorama_list, name='panoramas'),
    path('<slug:slug>/', views.panorama, name='panorama')
]

urlpatterns = [
    url_log_in,
    url_log_out,

    path('', views.index, name='index'),

    path('api/', include(api_patterns)),

    path('about/',
         TemplateView.as_view(template_name='about.html'),
         name='about'),

    path('copyright/',
         TemplateView.as_view(template_name='copyright.html'),
         name='copyright'),

    path('albums/', include(album_patterns)),
    path('tags/', include(tag_patterns)),

    path('panoramas/', include(panorama_patterns)),

    path('featured/', views.featured, name='featured'),
    path('wall/', views.wall, name='wall'),

    path('404/', views.debug404),
    path('500/', views.debug500),
]


if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]

    urlpatterns += static(settings.STATIC_URL)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
