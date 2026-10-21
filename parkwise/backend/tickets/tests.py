"""Entry / exit / block rules. Every test starts with an EMPTY lot (C08 blocked at both gates)."""
import json

from django.test import TestCase

from core import clock
from core.seed import load_seed_data


class ParkingRulesTest(TestCase):
    def setUp(self):
        load_seed_data()

    def post(self, url, body):
        return self.client.post(url, json.dumps(body), content_type="application/json")

    def enter(self, number, vehicle_type="4W", gate="Gate A"):
        return self.post("/api/entry/", {"vehicle_number": number, "vehicle_type": vehicle_type,
                                         "gate": gate})

    def block(self, number, blocked, gate="Gate A"):
        return self.post("/api/slots/block/", {"gate": gate, "number": number, "blocked": blocked})

    def test_lowest_free_slot_and_cleaned_number(self):
        data = self.enter("mh 12 gh 3456").json()
        self.assertEqual((data["slot"], data["gate"]), ("C01", "Gate A"))
        self.assertEqual(data["vehicle_number"], "MH12GH3456")
        self.assertEqual(data["ticket"], "PK-0001")

    def test_each_gate_has_its_own_slots(self):
        self.enter("AAAA1111", gate="Gate A")
        b = self.enter("BBBB2222", gate="Gate B").json()
        self.assertEqual((b["gate"], b["slot"]), ("Gate B", "C01"))  # Gate B has its own C01
        counts = self.client.get("/api/slots/?gate=Gate B").json()["counts"]
        self.assertEqual(counts["4W"]["free"], 6)  # 7 usable - 1 used

    def test_error_codes(self):
        self.assertEqual(self.enter("ab").status_code, 422)            # INVALID_VEHICLE
        self.enter("KA01AB1234")
        self.assertEqual(self.enter("KA01AB1234", gate="Gate B").json()["code"], "ALREADY_PARKED")
        self.assertEqual(self.post("/api/entry/", {}).status_code, 400)

    def test_two_wheeler_never_uses_four_wheeler_slot(self):
        for n in range(12):  # fill all 12 two-wheeler slots at Gate A
            self.enter(f"BIKE00{n:02d}", "2W")
        full = self.enter("BIKE9999", "2W")
        self.assertEqual((full.status_code, full.json()["code"]), (409, "LOT_FULL"))
        self.assertEqual(self.enter("BIKE9999", "2W", "Gate B").json()["slot"], "B01")

    def test_exit_flow(self):
        self.enter("TS08CD5678")
        clock.advance(90)  # 90 minutes -> still the base price, car Rs50
        info = self.client.get("/api/exit/lookup/?q=ts08 cd5678").json()
        self.assertEqual((info["fee"]["fee"], info["gate"]), (50, "Gate A"))
        receipt = self.post("/api/exit/collect/", {"q": "TS08CD5678", "payment_method": "UPI",
                                                   "gate": "Gate B"}).json()  # other gate collects
        self.assertEqual((receipt["amount"], receipt["exit_gate"]), (50, "Gate B"))
        again = self.post("/api/exit/collect/", {"q": receipt["ticket"], "payment_method": "UPI",
                                                 "gate": "Gate B"})
        self.assertEqual(again.json()["code"], "ALREADY_PAID")
        self.assertEqual(self.client.get("/api/exit/lookup/?q=TS08CD5678").status_code, 404)
        dash = self.client.get("/api/dashboard/?gate=Gate A").json()
        self.assertEqual((dash["total_collected_today"], dash["collected_by_gate"]["Gate B"]), (50, 50))

    def test_exit_with_last_four_characters(self):
        self.enter("KA01AB1234")
        self.assertEqual(self.client.get("/api/exit/lookup/?q=1234").json()["vehicle_number"], "KA01AB1234")
        self.enter("AAAA9999")
        self.enter("BBBB9999")
        self.assertEqual(self.client.get("/api/exit/lookup/?q=9999").status_code, 400)  # two matches

    def test_block_and_unblock_slot(self):
        self.assertEqual(self.block("C01", True).json()["is_blocked"], True)
        self.assertEqual(self.enter("CARS0001").json()["slot"], "C02")      # C01 skipped
        self.assertEqual(self.block("C02", True).status_code, 400)          # occupied: cannot block
        self.block("C01", False)
        self.assertEqual(self.enter("CARS0002").json()["slot"], "C01")      # C01 is back
        self.assertEqual(self.block("Z99", True).status_code, 400)          # unknown slot
        # blocking at Gate A does not touch Gate B
        self.assertEqual(self.client.get("/api/slots/?gate=Gate B").json()["counts"]["4W"]["free"], 7)
