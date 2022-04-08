from django.contrib import admin


class WatermarkAdmin(admin.ModelAdmin):
    fields = ('image', 'color', 'apply_to_size', 'created_date', 'updated_date')
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('pk', 'color', 'apply_to_size', 'created_date', 'updated_date')
