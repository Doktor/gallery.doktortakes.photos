from django.contrib import admin


class RequestAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'method', 'path', 'status_code', 'ip_address', 'user_agent')
    list_filter = ('method', 'status_code', 'user')
    search_fields = ('path', 'ip_address', 'user_agent', 'referer', 'user__username')

    readonly_fields = ('created_at', 'method', 'path', 'ip_address', 'user_agent', 'referer', 'status_code', 'user')
