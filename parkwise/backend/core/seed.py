"""Starting data: the parking slots only. The lot starts EMPTY (no vehicles).

Run it with `python manage.py seed_data`, or use "Clear all data" in the dev bar.
It deletes every visit and payment, restores the default slots and
restarts ticket numbering at PK-0001.
"""
from django.db import connection

from billing.models import Payment
from slots.services import ensure_slots
from tickets.models import Visit

from . import clock


def load_seed_data():
    clock.reset()
    Payment.objects.all().delete()
    Visit.objects.all().delete()
    # restart ticket numbering at PK-0001
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('tickets_visit', 'billing_payment')")

    ensure_slots()  # also puts every slot back to its default blocked/unblocked state
