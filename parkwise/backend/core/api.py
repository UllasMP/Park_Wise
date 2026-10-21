"""@json_api: a tiny decorator so every view stays short.

It checks the HTTP method, reads the JSON body, converts ApiError to a JSON
error response, and wraps the returned dict in JsonResponse.
A view may return `data` or `(data, status_code)`.
"""
import json
from functools import wraps

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .errors import ApiError, bad_request


def error_response(error):
    return JsonResponse({"code": error.code, "message": error.message}, status=error.status)


def read_json(request):
    """Return the JSON body as a dict (empty body -> {})."""
    if not request.body:
        return {}
    try:
        body = json.loads(request.body)
    except ValueError:
        raise bad_request("Request body must be valid JSON.")
    if not isinstance(body, dict):
        raise bad_request("Request body must be a JSON object.")
    return body


def json_api(*allowed_methods):
    def decorator(view):
        @csrf_exempt  # no login/cookies in this app, so CSRF is not needed
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            try:
                if request.method not in allowed_methods:
                    raise ApiError("METHOD_NOT_ALLOWED", "Method not allowed.", 405)
                request.json = read_json(request) if request.method == "POST" else {}
                result = view(request, *args, **kwargs)
                data, status = result if isinstance(result, tuple) else (result, 200)
                return JsonResponse(data, status=status)
            except ApiError as error:
                return error_response(error)
        return wrapper
    return decorator
