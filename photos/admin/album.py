from django import forms
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from photos.models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Album
        widgets = {'description': forms.Textarea}


class AlbumAdmin(MPTTModelAdmin):
    form = AlbumForm
    fieldsets = (
        ('Main', {
            'fields': ('name', 'slug', 'location', 'description',
                       'start', 'end', 'parent', 'tags', 'display_image_size'),
        }),
        ('Visibility', {
            'fields': ('access_level', 'access_code', 'users', 'groups'),
        }),
        ('Cover photo', {
            'fields': ('cover', 'preview'),
        }),
    )
    list_display = ('name', 'location', 'start', 'end', 'description', 'path')
    mptt_level_indent = 30
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('preview',)
    search_fields = ('name', 'location', 'description')

    def preview(self, album):
        """Creates a HTML element to preview the cover photo."""
        if album.cover:
            thumbnail = album.cover.get_display_image()

            return format_html('<a href="{}"><img height="300" src="{}"></a>',
                               thumbnail.image.url, thumbnail.image.url)
