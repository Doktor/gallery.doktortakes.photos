from django.contrib import admin

from .album import AlbumAdmin
from .file import FileAdmin
from .hero_photo import HeroPhotoAdmin
from .photo import PhotoAdmin
from .tag import TagAdmin
from .tagline import TaglineAdmin

from photos.models import Album, File, HeroPhoto, Photo, Tag, Tagline


admin.site.register(Album, AlbumAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(HeroPhoto, HeroPhotoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Tagline, TaglineAdmin)
admin.site.register(Photo, PhotoAdmin)
