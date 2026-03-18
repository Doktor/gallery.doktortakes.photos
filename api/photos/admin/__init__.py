from django.contrib import admin

from .album import AlbumAdmin
from .creator import CreatorAdmin
from .file import FileAdmin
from .hero_photo import HeroPhotoAdmin
from .license import LicenseAdmin
from .photo import PhotoAdmin
from .tag import TagAdmin
from .tagline import TaglineAdmin
from .taxon import TaxonAdmin
from .thumbnail import ThumbnailAdmin

from photos.models import Album, Creator, File, HeroPhoto, License, Photo, Tag, Tagline, Taxon, Thumbnail


admin.site.register(Album, AlbumAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(HeroPhoto, HeroPhotoAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Tagline, TaglineAdmin)
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
