from django.urls import path, register_converter

from core.converters import MD5HashConverter
from photos.api import views

register_converter(MD5HashConverter, 'md5')


api_patterns = [
    path('photos/featured/', views.get_featured_photos, name='api_featured_photos'),
    path('photos/search/', views.search_photos, name='search_photos'),
    path('photos/<md5:md5>/', views.PhotoDetail.as_view(), name='api_photo'),

    path('albums/<path:path>/photos/', views.AlbumPhotoList.as_view(), name='api_album_photos'),
    path('albums/<path:path>/', views.AlbumDetail.as_view(), name='api_album'),
    path('albums/', views.AlbumList.as_view(), name='api_albums'),

    path('tags/', views.TagList.as_view(), name='api_tags'),

    path('users/', views.UserList.as_view(), name='api_users'),
    path('groups/', views.GroupList.as_view(), name='api_groups'),

    path('me/', views.get_current_user, name='api_current_user'),
    path('me/password/', views.change_password, name='api_change_password'),

    path('recent/', views.get_recent),
]
