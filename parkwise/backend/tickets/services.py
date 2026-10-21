"""Entry logic + helper to find a visit by vehicle number or ticket number."""
import re

from django.db import transaction

from core import clock
from core.errors import (already_paid, already_parked, bad_request,
                         invalid_vehicle, lot_full, not_parked)
from core.lock import parking_lock
from core.vehicle import clean_vehicle_number, is_valid_vehicle_number
from slots.models import VEHICLE_TYPES
from slots.services import check_gate, find_free_slot

from .models import Visit

def ticket_dict(visit):
    return {
        "ticket": visit.ticket_number,
        "vehicle_number": visit.vehicle_number,
        "vehicle_type": visit.vehicle_type,
        "slot": visit.slot.number,
        "level": visit.slot.level,
        "entry_time": visit.entry_time.isoformat(),
        "gate": visit.slot.gate,
    }


def issue_ticket(raw_number, vehicle_type, gate):
    # --- 1. check the input -------------------------------------------
    check_gate(gate)  # the gate decides which parking area is used
    if not isinstance(raw_number, str) or not raw_number.strip():
        raise bad_request("vehicle_number is required.")
    if not isinstance(vehicle_type, str) or not vehicle_type:
        raise bad_request("vehicle_type is required.")

    vehicle_number = clean_vehicle_number(raw_number)
    if not is_valid_vehicle_number(vehicle_number):
        raise invalid_vehicle("Vehicle number must be 6 to 10 letters or digits.")
    if vehicle_type not in VEHICLE_TYPES:
        raise invalid_vehicle("vehicle_type must be '2W' or '4W'.")

    # --- 2. pick the slot (inside the lock: two gates can't clash) ------
    with parking_lock, transaction.atomic():
        if Visit.objects.filter(vehicle_number=vehicle_number, exit_time__isnull=True).exists():
            raise already_parked()

        slot = find_free_slot(vehicle_type, gate)  # only this gate's slots
        if slot is None:
            raise lot_full()

        visit = Visit.objects.create(
            vehicle_number=vehicle_number, vehicle_type=vehicle_type,
            slot=slot, entry_time=clock.now())
    return ticket_dict(visit)


def find_visit(query, for_payment=False):
    """Find a visit from what the operator typed.

    - 'PK-0142' (has a hyphen) is a ticket number.
    - anything else is a vehicle number (spaces/case ignored). The full number
      or just the last 4+ characters both work.
    Not inside -> NOT_PARKED. A closed ticket being paid again -> ALREADY_PAID.
    """
    if not isinstance(query, str) or not query.strip():
        raise bad_request("Enter a vehicle number or ticket number.")

    text = re.sub(r"\s+", "", query).upper()
    ticket_match = re.fullmatch(r"PK-(\d+)", text)

    if ticket_match:
        visit = Visit.objects.select_related("slot").filter(id=int(ticket_match.group(1))).first()
        if visit is None:
            raise not_parked()
        if not visit.is_inside:
            raise already_paid() if for_payment else not_parked()
        return visit

    inside = Visit.objects.select_related("slot").filter(exit_time__isnull=True)

    # 1) full vehicle number
    visit = inside.filter(vehicle_number=text).first()
    if visit:
        return visit

    # 2) last characters, e.g. just "1234" (at least 4 typed)
    if len(text) >= 4:
        matches = list(inside.filter(vehicle_number__endswith=text)[:5])
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            numbers = ", ".join(v.vehicle_number for v in matches)
            raise bad_request(f"More than one vehicle matches ({numbers}). Type more characters.")
    raise not_parked()
