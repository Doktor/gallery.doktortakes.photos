from typing import Callable

from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views import View

import functools
import json
from json import JSONDecodeError


class APIError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)

        self.message = message
        self.status = status

    def to_response(self) -> JsonResponse:
        return JsonResponse({'error': self.message}, status=self.status)


def api_wrapper(f: Callable) -> Callable:
    @functools.wraps(f)
    def wrapper(request: HttpRequest, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except APIError as e:
            return e.to_response()

    return wrapper


@method_decorator(api_wrapper, name='dispatch')
class APIView(View):
    def _get_data(self, request: HttpRequest):
        content_type = request.META.get('CONTENT_TYPE', '')

        if not content_type.startswith('application/json'):
            raise APIError("Invalid content type.")

        try:
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            raise APIError("Invalid JSON data.")

        return data
