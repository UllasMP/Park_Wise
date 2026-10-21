"""Dev-only tools (only work while DEBUG=True)."""
from django.conf import settings

from . import clock
from .api import json_api
from .errors import ApiError, bad_request
from .seed import load_seed_data


def _check_dev_mode():
    if not settings.DEBUG:
        raise ApiError("NOT_FOUND", "Dev tools are disabled.", 404)


@json_api("GET", "POST")
def dev_clock(request):
    """GET: show server time. POST {"minutes": 60}: move the clock forward."""
    _check_dev_mode()
    if request.method == "POST":
        minutes = request.json.get("minutes")
        if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes <= 0:
            raise bad_request("minutes must be a positive whole number.")
        clock.advance(minutes)
    return {"server_time": clock.now().isoformat(), "offset_minutes": clock.offset_minutes()}


@json_api("POST")
def dev_reset(request):
    """Wipe all visits/payments and restore the default slots."""
    _check_dev_mode()
    load_seed_data()
    return {"message": "All data cleared."}
