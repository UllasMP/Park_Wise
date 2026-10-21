from core.api import json_api

from .services import issue_ticket


@json_api("POST")
def entry(request):
    """POST /api/entry/  {vehicle_number, vehicle_type, gate} -> ticket"""
    body = request.json
    ticket = issue_ticket(body.get("vehicle_number"), body.get("vehicle_type"), body.get("gate"))
    return ticket, 201
