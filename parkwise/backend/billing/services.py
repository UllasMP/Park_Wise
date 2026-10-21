"""Exit screen logic: show the fee, then collect it and release the slot."""
from django.db import transaction

from core import clock
from core.errors import bad_request
from core.lock import parking_lock
from slots.services import check_gate
from tickets.services import find_visit

from .fee_calculator import calculate_fee, stay_minutes
from .models import Payment

PAYMENT_METHODS = ["CASH", "UPI"]


def exit_preview(query):
    """What the operator sees before paying: slot, times, stay, fee + breakdown."""
    visit = find_visit(query)
    now = clock.now()
    minutes = stay_minutes(visit.entry_time, now)
    return {
        "ticket": visit.ticket_number,
        "vehicle_number": visit.vehicle_number,
        "vehicle_type": visit.vehicle_type,
        "slot": visit.slot.number,
        "gate": visit.slot.gate,  # gate where the vehicle entered
        "entry_time": visit.entry_time.isoformat(),
        "time_now": now.isoformat(),
        "stay_minutes": minutes,
        "fee": calculate_fee(visit.vehicle_type, minutes),
    }


def collect_payment(query, method, gate):
    """Re-calculate the fee NOW, save the payment, free the slot, return a receipt."""
    if not isinstance(method, str) or method.upper() not in PAYMENT_METHODS:
        raise bad_request("payment_method must be 'CASH' or 'UPI'.")
    check_gate(gate)

    with parking_lock, transaction.atomic():
        visit = find_visit(query, for_payment=True)   # closed ticket -> ALREADY_PAID
        now = clock.now()
        minutes = stay_minutes(visit.entry_time, now)
        fee = calculate_fee(visit.vehicle_type, minutes)["fee"]

        payment = Payment.objects.create(
            visit=visit, amount=fee, method=method.upper(),
            stay_minutes=minutes, gate=gate, paid_at=now)
        visit.exit_time = now       # closing the visit frees the slot
        visit.save()                # (the visit record is kept, never deleted)
    return receipt_dict(payment)


def receipt_dict(payment):
    visit = payment.visit
    return {
        "ticket": visit.ticket_number,
        "vehicle_number": visit.vehicle_number,
        "vehicle_type": visit.vehicle_type,
        "slot": visit.slot.number,
        "gate": visit.slot.gate,        # entry gate
        "exit_gate": payment.gate,      # gate where it was paid
        "entry_time": visit.entry_time.isoformat(),
        "exit_time": visit.exit_time.isoformat(),
        "stay_minutes": payment.stay_minutes,
        "amount": payment.amount,
        "payment_method": payment.method,
    }
