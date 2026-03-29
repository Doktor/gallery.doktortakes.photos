import pstats

try:
    import cProfile as profile
except ImportError:
    import profile

from io import StringIO

from django.conf import settings
from django.http import HttpResponse

from photos.models import Request


class ProfilerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (settings.DEBUG and 'profile' in request.GET):
            return self.get_response(request)

        profiler = profile.Profile()
        profiler.runcall(self.get_response, request)

        buffer = StringIO()
        stats = pstats.Stats(profiler, stream=buffer)

        stats.sort_stats('cumulative', 'ncalls')
        stats.print_stats(100)

        return HttpResponse('<pre>%s</pre>' % buffer.getvalue())


REQUEST_LOGGING_EXCLUDE_PREFIXES = [
    '/__debug__/'
]


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if any(request.path.startswith(prefix) for prefix in REQUEST_LOGGING_EXCLUDE_PREFIXES):
            return response

        if (forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR')):
            ip_address = forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        Request.objects.create(
            path=request.path,
            method=request.method,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referer=request.META.get('HTTP_REFERER', ''),
            status_code=response.status_code,
            user=request.user if request.user.is_authenticated else None,
        )

        return response
