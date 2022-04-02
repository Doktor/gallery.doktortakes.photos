from django.contrib import admin


class ThumbnailAdmin(admin.ModelAdmin):
    fields = ('type', 'image', 'is_watermarked', 'width', 'height', 'file_size', 'created_date', 'updated_date')
    readonly_fields = ('image', 'is_watermarked', 'width', 'height', 'file_size', 'created_date', 'updated_date')
    list_display = ('pk', 'photo_id', 'image', 'width', 'height', 'file_size', 'created_date', 'updated_date')
