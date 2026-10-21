from django.db import models
from django.db.models import Q

from slots.models import Slot


class Visit(models.Model):
    """One visit = one ticket. The gate comes from the slot (slot.gate). Never deleted; exit_time is filled when paid."""
    vehicle_number = models.CharField(max_length=10)  # already cleaned
    vehicle_type = models.CharField(max_length=2)     # "2W" / "4W"
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)  # null = still inside

    class Meta:
        constraints = [
            # Safety net: a slot can hold only ONE vehicle that is still inside
            models.UniqueConstraint(
                fields=["slot"], condition=Q(exit_time__isnull=True),
                name="one_vehicle_per_slot"),
            # Safety net: the same vehicle cannot be inside twice
            models.UniqueConstraint(
                fields=["vehicle_number"], condition=Q(exit_time__isnull=True),
                name="vehicle_inside_only_once"),
        ]

    @property
    def ticket_number(self):
        return f"PK-{self.id:04d}"  # running number: PK-0001, PK-0002 ...

    @property
    def is_inside(self):
        return self.exit_time is None
