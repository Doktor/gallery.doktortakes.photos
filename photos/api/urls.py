from django.urls import include, path, register_converter

from photos.api import views
from photos.api.views import manage
from photos.converters import MD5HashConverter

register_converter(MD5HashConverter, 'md5')


manage_patterns = [
    path('albums/<path:path>/photos/', manage.ManageAlbumPhotoList.as_view(), name='api_manage_album_photos'),
    path('albums/<path:path>/', manage.ManageAlbumDetail.as_view(), name='api_manage_album'),
    path('albums/', manage.ManageAlbumList.as_view(), name='api_manage_albums'),

    path('photos/recent/', manage.ManageRecentPhotoList.as_view(), name='recent_photos'),
    path('photos/<md5:md5>/', manage.ManagePhotoDetail.as_view(), name='api_manage_photo'),
    path('photos/<md5:md5>/thumbnails/', manage.ManageThumbnailList.as_view(), name='api_thumbnail'),
    path('photos/<md5:md5>/taxa/<str:catalog_id>/', manage.ManagePhotoTaxonDetail.as_view()),
    path('photos/<md5:md5>/taxa/', manage.ManagePhotoTaxonList.as_view()),

    path('users/', manage.UserList.as_view(), name='api_users'),
    path('groups/', manage.GroupList.as_view(), name='api_groups'),

    path('taxa/import/', manage.ImportTaxon.as_view(), name='api_import_taxa'),
    path('taxa/', manage.ManageTaxonList.as_view(), name='api_manage_taxa'),
]

api_patterns = [
    path('photos/search/', views.search_photos, name='search_photos'),

    path('photos/<md5:md5>/', views.PhotoDetail.as_view(), name='api_photo'),

    path('albums/<path:path>/photos/', views.AlbumPhotoList.as_view(), name='api_album_photos'),
    path('albums/<path:path>/', views.AlbumDetail.as_view(), name='api_album'),
    path('albums/', views.AlbumList.as_view(), name='api_albums'),

    path('tags/', views.TagList.as_view(), name='api_tags'),

    path('taxa/species/', views.SpeciesList.as_view()),
    path('taxa/<str:catalog_id>/photos/', views.TaxonPhotoList.as_view(), name='api_taxa'),
    path('taxa/', views.TaxonList.as_view(), name='api_taxa'),

    path('me/', views.get_current_user, name='api_current_user'),
    path('me/password/', views.change_password, name='api_change_password'),

    path('heroPhotos/', views.get_hero_photos, name='api_hero_photos'),
    path('taglines/random/', views.get_tagline, name='api_tagline'),

    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('authenticate/', views.get_api_token, name='get_api_token'),

    path('manage/', include(manage_patterns)),
]
