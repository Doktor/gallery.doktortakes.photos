from django import forms
from django.contrib import admin
from django.utils.html import format_html

from photos.fields import JSONField, JSONWidget
from photos.models import Album, Photo, Panorama


class AlbumForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Album
        widgets = {'description': forms.Textarea}


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    fieldsets = (
        ('Main', {
            'fields': ('name', 'slug', 'location', 'description',
                       'start', 'end', 'parent'),
        }),
        ('Visibility', {
            'fields': ('hidden', 'password')
        }),
        ('Cover photo', {
            'fields': ('cover', 'preview')
        }),
    )
    list_display = ('name', 'location', 'start', 'end',
                    'description', 'get_path')
    ordering = ('-start',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('preview',)
    search_fields = ('name', 'location', 'description')

    def preview(self, album):
        """Creates a HTML element to preview the cover photo."""
        if album.cover:
            return format_html('<a href="{}"><img height="300" src="{}"></a>',
                               album.cover.image.url, album.cover.thumbnail.url)

    preview.short_description = 'Preview'


class PhotoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONWidget},
    }
    fieldsets = (
        ('Image', {
            'fields': ('image', 'preview',
                       'md5', 'width', 'height', 'file_size', 'exif')
        }),
        ('Other', {
            'fields': ('crop', 'rating', 'album')
        }),
        ('Dates', {
            'fields': ('taken', 'edited')
        }),
    )
    list_display = ('__str__', 'album_name', 'width', 'height',
                    'file_size', 'taken', 'edited', 'rating')
    ordering = ('-taken',)
    readonly_fields = ('preview', 'md5', 'width', 'height', 'file_size',
                       'taken', 'edited')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields['exif'].disabled = True
        return form

    def preview(self, photo):
        return format_html('<a href="{}"><img height="300" src="{}"></a>',
                           photo.image.url, photo.thumbnail.url)

    preview.short_description = 'Preview'

    def album_name(self, photo):
        return photo.album.name

    album_name.short_description = 'Album name'


class PanoramaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Event', {
            'fields': ('name', 'slug', 'location', 'description')
        }),
        ('Image', {
            'fields': ('image', 'thumbnail', 'preview',
                       'md5', 'width', 'height', 'file_size')
        }),
        ('Dates', {
            'fields': ('timezone', 'taken', 'edited', 'uploaded')
        }),
    )
    list_display = ('name', 'location', 'taken', 'md5',
                    'width', 'height', 'file_size')
    ordering = ('-taken',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('thumbnail', 'preview', 'md5', 'width', 'height',
                       'file_size', 'taken', 'edited', 'uploaded')

    def preview(self, pano):
        return format_html('<a href="{0}"><img width="1000" src="{0}"></a>',
                           pano.thumbnail.url)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Panorama, PanoramaAdmin)
