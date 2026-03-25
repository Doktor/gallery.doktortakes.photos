from django.contrib import admin


class RequestAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'method', 'path', 'status_code', 'ip_address', 'user_agent')
    list_filter = ('method', 'status_code')
    search_fields = ('path', 'ip_address', 'user_agent', 'referer')

    readonly_fields = ('created_at', 'method', 'path', 'ip_address', 'user_agent', 'referer', 'status_code')
