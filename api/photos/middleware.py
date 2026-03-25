import pstats

try:
    import cProfile as profile
except ImportError:
    import profile

from io import StringIO

import django
from django.conf import settings
from django.http import HttpResponse

from django.utils.deprecation import MiddlewareMixin

from photos.models import Request


class ProfilerMiddleware(MiddlewareMixin):
    def should_handle(self, request):
        return settings.DEBUG and 'profile' in request.GET

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if not self.should_handle(request):
            return

        self.profiler = profile.Profile()

        args = (request,) + callback_args

        try:
            result = self.profiler.runcall(callback, *args, **callback_kwargs)
        except Exception as exc:
            raise exc

        return result

    def process_response(self, request, response):
        if not self.should_handle(request):
            return response

        buffer = StringIO()
        stats = pstats.Stats(self.profiler, stream=buffer)

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
        )

        return response
