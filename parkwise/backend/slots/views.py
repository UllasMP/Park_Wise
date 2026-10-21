from core.api import json_api

from .services import check_gate, set_slot_blocked, slot_map


@json_api("GET")
def slot_map_view(request):
    """GET /api/slots/?gate=Gate A -> free counts + every slot of that gate."""
    return slot_map(check_gate(request.GET.get("gate")))


@json_api("POST")
def slot_block_view(request):
    """POST /api/slots/block/ {gate, number: "C03", blocked: true|false}"""
    body = request.json
    return set_slot_blocked(body.get("gate"), body.get("number"), body.get("blocked"))
