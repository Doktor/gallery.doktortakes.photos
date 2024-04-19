from django.contrib import admin


class LicenseAdmin(admin.ModelAdmin):
    fields = ('display_name', 'full_name', 'description', 'link')
    list_display = ('display_name', 'full_name', 'description', 'link')
