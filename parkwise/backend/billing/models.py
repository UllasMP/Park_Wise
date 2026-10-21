from django.db import models

from tickets.models import Visit


class Payment(models.Model):
    """Saved when an operator collects the fee. One payment per visit."""
    visit = models.OneToOneField(Visit, on_delete=models.PROTECT, related_name="payment")
    amount = models.PositiveIntegerField()        # whole rupees
    method = models.CharField(max_length=4)       # "CASH" / "UPI"
    stay_minutes = models.PositiveIntegerField()
    gate = models.CharField(max_length=10)        # gate where the money was collected
    paid_at = models.DateTimeField()
