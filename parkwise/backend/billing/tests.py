"""Fee tests for the pricing rules (see fee_calculator.py)."""
from django.test import SimpleTestCase

from .fee_calculator import calculate_fee


class FeeExamplesTest(SimpleTestCase):
    def test_examples(self):
        # (minutes, expected bike fee, expected car fee)
        examples = [
            (1, 30, 50),        # base price even for a short stay
            (120, 30, 50),      # exactly 2 hours: still base
            (121, 40, 70),      # 1 extra hour (part of an hour counts)
            (180, 40, 70),
            (181, 50, 90),
            (320, 70, 130),     # 200 min after base -> 4 extra hours
            (1440, 250, 490),   # exactly 24 hours: no day fee yet
            (1441, 300, 540),   # crossed 24 hours: +Rs50
            (1560, 300, 540),   # 26 hours
            (2880, 300, 540),   # exactly 48 hours
            (2881, 350, 590),   # crossed 48 hours: +Rs50 again
        ]
        for minutes, bike, car in examples:
            self.assertEqual(calculate_fee("2W", minutes)["fee"], bike, f"bike {minutes}")
            self.assertEqual(calculate_fee("4W", minutes)["fee"], car, f"car {minutes}")
