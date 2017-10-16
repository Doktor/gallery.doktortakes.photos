"""photos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from photos import views

handler404 = 'photos.views.handler404'
handler500 = 'photos.views.handler500'

album_patterns = [
    url(r'^$', views.directory, name='directory'),
    url(r'^all/$', views.all_photos, name='all'),

    url(r'^(?P<path>[a-z0-9-/]+)/edit/$',
        views.edit_album, name='edit_album'),
    url(r'^(?P<path>[a-z0-9-/]+)/delete/$',
        views.delete_album, name='delete_album'),
    url(r'^(?P<path>[a-z0-9-/]+)/upload/$',
        views.upload_photo, name='upload'),

    url(r'^(?P<path>[a-z0-9-/]+)/$',
        views.album, name='album'),
    url(r'^(?P<path>[a-z0-9-/]+)/(?P<md5>[a-f0-9]{32})$',
        views.photo, name='photo'),

    url(r'^(?P<path>[a-z0-9-/]+)/(?P<md5>[a-f0-9]{32})/info$',
        views.photo_info, name='info'),
    url(r'^(?P<path>[a-z0-9-/]+)/(?P<md5>[a-f0-9]{32})/download$',
        views.photo_download, name='download'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^commissions/$',
        TemplateView.as_view(template_name='commissions.html'),
        name='commissions'),

    url(r'login/$',
        views.site_login, name='login'),
    url(r'logout/$',
        views.site_logout, name='logout'),

    url(r'^edit/$', views.edit_content, name='edit'),
    url(r'^new/$', views.new_album, name='new_album'),

    url(r'^albums/', include(album_patterns)),

    url(r'^404/$', views.debug404),
    url(r'^500/$', views.debug500),
]

if settings.DEBUG:
    urlpatterns += [url(r'^admin/', admin.site.urls)]

urlpatterns += [
    url(r'^(?P<path>[a-z0-9-/]+)/$',
        views.album_redirect, name='album_old'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
