from django.contrib import admin


class TaglineAdmin(admin.ModelAdmin):
    fields = ('text',)
    list_display = ('pk', 'text', 'created_date', 'updated_date')