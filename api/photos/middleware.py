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
