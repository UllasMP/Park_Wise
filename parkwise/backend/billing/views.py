from core.api import json_api

from .services import collect_payment, exit_preview


@json_api("GET")
def exit_lookup(request):
    """GET /api/exit/lookup/?q=<vehicle or ticket> -> details + fee if paid now"""
    return exit_preview(request.GET.get("q"))


@json_api("POST")
def exit_collect(request):
    """POST /api/exit/collect/ {q, payment_method, gate} -> receipt"""
    body = request.json
    return collect_payment(body.get("q"), body.get("payment_method"), body.get("gate"))
