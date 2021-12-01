from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from photos.fields import JSONField, JSONWidget


class PhotoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONWidget},
    }
    fieldsets = (
        ('Image', {
            'fields': ('original', 'original_filename', 'exif')
        }),
        ('Display image', {
            'fields': ('image', 'square_thumbnail', 'thumbnail',
                       'preview', 'watermark',
                       'md5', 'dimensions', 'file_size')
        }),
        ('Other', {
            'fields': ('rating', 'album')
        }),
        ('Dates', {
            'fields': ('taken', 'edited')
        }),
    )
    list_display = ('__str__', 'original_filename', 'album_name',
                    'width', 'height', 'file_size', 'taken', 'uploaded')
    ordering = ('-taken',)
    readonly_fields = (
        'image', 'square_thumbnail', 'thumbnail', 'preview',
        'md5', 'dimensions', 'file_size', 'taken', 'edited')

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
        return format_html('<a href="{}"><img height="300" src="{}"></a>',
                           photo.image.url, photo.image.url)