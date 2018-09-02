from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from auth.urls import url_log_in, url_log_out
from photos import api, views

handler404 = 'photos.views.handler404'
handler500 = 'photos.views.handler500'

album_patterns = [
    url(r'^$', views.album_list, name='albums'),
    url(r'^search/$', views.search_photos, name='search'),

    url(r'^(?P<path>[a-z0-9-/]+)/edit/$',
        views.edit_album, name='edit_album'),
    url(r'^(?P<path>[a-z0-9-/]+)/upload/$',
        views.upload_photo, name='upload'),

    url(r'^(?P<path>[a-z0-9-/]+)/$',
        views.album, name='album'),
    url(r'^(?P<path>[a-z0-9-/]+)/(?P<md5>[a-f0-9]{32})$',
        views.photo, name='photo'),

    url(r'^(?P<path>[a-z0-9-/]+)/(?P<md5>[a-f0-9]{32})/download$',
        views.photo_download, name='download'),
]

tag_patterns = [
    url(r'^$', views.tags, name='tags'),
    url(r'^(?P<slug>[a-z0-9-]+)$', views.tag, name='tag'),
]

api_patterns = [
    url(r'^photo/$', api.PhotoView.as_view(), name='api_photo'),

    url(r'^photo/previous/$', api.previous_photo, name='previous_photo'),
    url(r'^photo/next/$', api.next_photo, name='next_photo'),
    url(r'^photo/first/$', api.first_photo, name='first_photo'),
    url(r'^photo/last/$', api.last_photo, name='last_photo'),

    url(r'^album/$', api.AlbumView.as_view(), name='api_album'),

    url(r'^album/photos/', api.get_album_photos, name='get_album_photos'),

    url(r'^search/$', api.search_photos, name='search_photos'),
]

panorama_patterns = [
    url(r'^$', views.panorama_list, name='panoramas'),
    url(r'^(?P<slug>[a-z0-9-]+)$', views.panorama, name='panorama')
]

urlpatterns = [
    url_log_in,
    url_log_out,

    url(r'^$', views.index, name='index'),

    url(r'^api/', include(api_patterns)),

    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^copyright/$',
        TemplateView.as_view(template_name='copyright.html'),
        name='copyright'),

    url(r'^edit/$', views.edit_content, name='edit'),
    url(r'^new/$', views.new_album, name='new_album'),

    url(r'^albums/', include(album_patterns)),

    url(r'^tags/', include(tag_patterns)),

    url(r'^panoramas/', include(panorama_patterns)),

    url(r'^featured/', views.featured, name='featured'),
    url(r'^wall/', views.wall, name='wall'),

    url(r'^404/$', views.debug404),
    url(r'^500/$', views.debug500),
]


if settings.DEBUG:
    urlpatterns += [url(r'^admin/', admin.site.urls)]

    urlpatterns += static(settings.STATIC_URL)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
