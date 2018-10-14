from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter
from django.views.generic import TemplateView

from auth.urls import url_log_in, url_log_out
from core.converters import MD5HashConverter
from photos import api, views

handler404 = 'photos.views.handler_404'
handler500 = 'photos.views.handler_500'

register_converter(MD5HashConverter, 'md5')

album_patterns = [
    path('', views.view_albums, name='albums'),

    path('new/', views.new_album, name='new_album'),
    path('edit/', views.edit_albums, name='edit_albums'),

    path('search/', views.search_photos, name='search'),

    path('<path:path>/edit/', views.edit_album, name='edit_album'),

    path('<path:path>/', views.view_album, name='album'),
    path('<path:path>/<md5:md5>', views.view_photo, name='photo'),
    path('<path:path>/<md5:md5>/download', views.download_photo, name='download'),
]

tag_patterns = [
    path('', views.view_tags, name='tags'),
    path('<slug:slug>/', views.view_tag, name='tag'),
]

api_patterns = [
    path('search/', api.search_photos, name='search_photos'),

    path('<path:path>/photo/', api.PhotoView.as_view(), name='api_photo'),
    path('<path:path>/upload/', api.upload_photo, name='upload_photo'),

    path('<path:path>/previous/', api.previous_photo, name='previous_photo'),
    path('<path:path>/next/', api.next_photo, name='next_photo'),
    path('<path:path>/first/', api.first_photo, name='first_photo'),
    path('<path:path>/last/', api.last_photo, name='last_photo'),

    path('<path:path>/photos/', api.get_album_photos, name='get_album_photos'),
    path('<path:path>/', api.AlbumView.as_view(), name='api_album'),
    path('', api.AlbumView.as_view(), name='api_new_album'),
]

user_patterns = [
    path('', views.view_users, name='users'),
    path('<slug:slug>/', views.view_user, name='user'),
    path('<slug:slug>/change-password/', views.ChangePasswordView.as_view(), name='password'),
]

panorama_patterns = [
    path('', views.panorama_list, name='panoramas'),
    path('<slug:slug>/', views.panorama, name='panorama')
]

urlpatterns = [
    url_log_in,
    url_log_out,

    path('', views.index, name='index'),

    path('about/',
         TemplateView.as_view(template_name='about.html'),
         name='about'),

    path('admin/', admin.site.urls),

    path('copyright/',
         TemplateView.as_view(template_name='copyright.html'),
         name='copyright'),

    path('albums/', include(album_patterns)),
    path('api/albums/', include(api_patterns)),
    path('tags/', include(tag_patterns)),

    path('users/', include(user_patterns)),

    path('panoramas/', include(panorama_patterns)),

    path('featured/', views.featured, name='featured'),
    path('wall/', views.wall, name='wall'),

    path('404/', views.debug_404, name='debug_404'),
    path('500/', views.debug_500, name='debug_500'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
