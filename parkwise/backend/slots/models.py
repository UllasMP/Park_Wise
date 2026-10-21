from django.db import models

TWO_WHEELER = "2W"
FOUR_WHEELER = "4W"
VEHICLE_TYPES = [TWO_WHEELER, FOUR_WHEELER]

# Each gate has its OWN parking area: 12 two-wheeler + 8 four-wheeler slots.
GATES = ["Gate A", "Gate B"]


class Slot(models.Model):
    """One parking slot, e.g. Gate A / B01. Slot numbers repeat for each gate."""
    gate = models.CharField(max_length=10)      # "Gate A" / "Gate B"
    number = models.CharField(max_length=3)     # B01.. (2W) or C01.. (4W)
    slot_type = models.CharField(max_length=2)  # "2W" or "4W"
    level = models.CharField(max_length=20)     # "Ground" / "Level 1"
    is_blocked = models.BooleanField(default=False)  # blocked slots are never given out

    class Meta:
        # B01 can exist once per gate, but not twice in the same gate
        unique_together = ("gate", "number")

    def __str__(self):
        return f"{self.gate} {self.number}"
