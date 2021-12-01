from django.contrib import admin
from django.utils.html import format_html


class HeroPhotoAdmin(admin.ModelAdmin):
    fields = (
        'image', 'preview', 'title', 'description', 'x_position',
        'created_date', 'updated_date',
    )
    list_display = (
        'pk', 'image', 'title', 'description', 'x_position',
        'created_date', 'updated_date',
    )
    readonly_fields = (
        'preview',
        'created_date', 'updated_date',
    )

    def preview(self, photo):
        url = photo.image.url
        return format_html('<a href="{}"><img height="300" src="{}"></a>', url, url)