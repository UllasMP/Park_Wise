"""Slot business logic: create slots, find a free one, build the slot map."""
from core.errors import bad_request
from core.lock import parking_lock

from .models import FOUR_WHEELER, GATES, TWO_WHEELER, Slot


def check_gate(gate):
    """Every request must name a valid gate."""
    if gate not in GATES:
        raise bad_request("gate must be 'Gate A' or 'Gate B'.")
    return gate


def ensure_slots():
    """For EACH gate: B01-B12 (2W, ground) and C01-C08 (4W, level 1).

    C08 starts blocked (operators can block/unblock any slot later).
    update_or_create also resets the blocked flag to this default.
    """
    for gate in GATES:
        for n in range(1, 13):
            Slot.objects.update_or_create(
                gate=gate, number=f"B{n:02d}",
                defaults={"slot_type": TWO_WHEELER, "level": "Ground"})
        for n in range(1, 9):
            Slot.objects.update_or_create(
                gate=gate, number=f"C{n:02d}",
                defaults={"slot_type": FOUR_WHEELER, "level": "Level 1", "is_blocked": n == 8})


def _occupied_slot_ids():
    from tickets.models import Visit  # imported here to avoid a circular import
    return set(Visit.objects.filter(exit_time__isnull=True).values_list("slot_id", flat=True))


def find_free_slot(vehicle_type, gate):
    """Lowest-numbered free slot of the SAME type, inside this gate's parking area.

    A 2-wheeler only ever gets a 2-wheeler slot and a 4-wheeler only a
    4-wheeler slot (no overflow). Blocked slots are skipped.
    Returns None when that type is full at this gate (-> LOT_FULL).
    """
    return (Slot.objects.filter(gate=gate, slot_type=vehicle_type, is_blocked=False)
            .exclude(id__in=_occupied_slot_ids()).order_by("number").first())


def free_counts(gate):
    """{"2W": {"free": 1, "total": 12}, "4W": {...}} for one gate (blocked not counted)."""
    occupied = _occupied_slot_ids()
    counts = {}
    for slot_type in (TWO_WHEELER, FOUR_WHEELER):
        usable = Slot.objects.filter(gate=gate, slot_type=slot_type, is_blocked=False)
        counts[slot_type] = {"free": usable.exclude(id__in=occupied).count(),
                             "total": usable.count()}
    return counts


def slot_map(gate):
    """Everything the frontend needs to draw one gate's slot map."""
    from tickets.models import Visit
    inside = {v.slot_id: v for v in Visit.objects.filter(slot__gate=gate, exit_time__isnull=True)}
    slots = []
    for slot in Slot.objects.filter(gate=gate).order_by("number"):
        visit = inside.get(slot.id)
        status = "blocked" if slot.is_blocked else ("occupied" if visit else "free")
        slots.append({
            "number": slot.number,
            "type": slot.slot_type,
            "level": slot.level,
            "status": status,
            "vehicle_number": visit.vehicle_number if visit else None,
            "ticket": visit.ticket_number if visit else None,  # used to open ticket details
        })
    return {"gate": gate, "counts": free_counts(gate), "slots": slots}


def set_slot_blocked(gate, number, blocked):
    """Block or unblock one slot (e.g. for repairs). Blocked slots are never given out."""
    check_gate(gate)
    if not isinstance(number, str) or not isinstance(blocked, bool):
        raise bad_request("number must be text and blocked must be true or false.")

    with parking_lock:  # so a slot cannot be blocked while an entry is picking it
        slot = Slot.objects.filter(gate=gate, number=number.strip().upper()).first()
        if slot is None:
            raise bad_request(f"{gate} has no slot {number}.")
        if blocked and slot.id in _occupied_slot_ids():
            raise bad_request("A vehicle is parked in this slot. Release it before blocking.")
        slot.is_blocked = blocked
        slot.save()
    return {"gate": gate, "number": slot.number, "is_blocked": slot.is_blocked}
