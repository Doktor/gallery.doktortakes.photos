from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from photos.models import Photo
from photos.models.photo.thumbnail import THUMBNAIL_SMALL_SQUARE


class PhotoTaxonInline(admin.TabularInline):
    model = Photo.taxa.through
    extra = 1


class PhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Image', {
            'fields': ('original', 'original_filename', 'exif')
        }),
        ('Display image', {
            'fields': ('preview', 'md5', 'dimensions', 'file_size')
        }),
        ('Other', {
            'fields': ('album', 'order')
        }),
        ('Dates', {
            'fields': ('taken', 'edited')
        }),
    )
    inlines = (
        PhotoTaxonInline,
    )
    list_display = ('__str__', 'original_filename', 'album_name',
                    'order', 'width', 'height', 'file_size', 'taken', 'uploaded')
    ordering = ('-taken',)
    readonly_fields = ('preview', 'md5', 'dimensions', 'file_size', 'taken', 'edited')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields['exif'].disabled = True
        return form

    # Custom fields

    def album_name(self, photo):
        return photo.album.name

    def dimensions(self, photo):
        return mark_safe(f"{photo.width} &times; {photo.height}")

    def preview(self, photo):
        thumbnail = photo.get_thumbnail(THUMBNAIL_SMALL_SQUARE)
        display = photo.get_meta_thumbnail()

        return format_html('<a href="{}"><img height="300" src="{}"></a>',
                           display.image.url, thumbnail.image.url)
