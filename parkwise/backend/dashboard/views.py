from django.db.models import Sum
from django.utils import timezone

from billing.models import Payment
from billing.services import receipt_dict
from core import clock
from core.api import json_api
from slots.models import GATES
from slots.services import check_gate, free_counts


@json_api("GET")
def dashboard(request):
    """GET /api/dashboard/?gate=Gate A

    free_slots           -> for the selected gate
    total_collected_today-> all gates together
    collected_by_gate    -> money collected at each gate
    exits_today          -> every exit today, newest first
    """
    gate = check_gate(request.GET.get("gate"))
    today = timezone.localdate(clock.now())
    payments = (Payment.objects.filter(paid_at__date=today)
                .select_related("visit", "visit__slot").order_by("-paid_at"))

    by_gate = {g: payments.filter(gate=g).aggregate(t=Sum("amount"))["t"] or 0 for g in GATES}
    return {
        "free_slots": free_counts(gate),
        "total_collected_today": sum(by_gate.values()),
        "collected_by_gate": by_gate,
        "exits_today": [receipt_dict(p) for p in payments],
    }
