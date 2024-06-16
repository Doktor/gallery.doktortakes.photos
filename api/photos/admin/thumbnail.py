from django.contrib import admin


class ThumbnailAdmin(admin.ModelAdmin):
    fields = ('type', 'image', 'width', 'height', 'file_size', 'created_date', 'updated_date')
    readonly_fields = ('image', 'width', 'height', 'file_size', 'created_date', 'updated_date')
    list_display = ('pk', 'photo_id', 'image', 'type', 'width', 'height', 'file_size', 'created_date', 'updated_date')
