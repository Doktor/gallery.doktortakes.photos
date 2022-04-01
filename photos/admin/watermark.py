from django.contrib import admin


class WatermarkAdmin(admin.ModelAdmin):
    fields = ('image', 'color', 'width', 'height', 'created_date', 'updated_date')
    readonly_fields = ('width', 'height', 'created_date', 'updated_date')
    list_display = ('pk', 'color', 'width', 'height', 'created_date', 'updated_date')
