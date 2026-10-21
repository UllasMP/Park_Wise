# Step 5 - Fees, exit and payment (`backend/billing`)

**`fee_calculator.py`** is pure maths (no database), so it is easy to test.
All prices are constants at the top of the file - change them there if the rules change.

| | Bike (2W) | Car (4W) |
|---|---|---|
| Base price (first 2 hours) | Rs30 | Rs50 |
| Each extra hour after 2 hours | Rs10 | Rs20 |
| Each extra 24 hours after the first 24 hours | Rs50 | Rs50 |

Steps:
1. minutes = ceil(seconds / 60)
2. First 24 hours: `base + extra_hours x hourly`, `extra_hours = ceil((minutes - 120) / 60)` (never below 0)
3. `extra_days = ceil(minutes / 1440) - 1`; add `extra_days x Rs50`

Examples (bike / car): 120 min = 30 / 50, 121 min = 40 / 70, 24h = 250 / 490,
24h 1min = 300 / 540, 48h 1min = 350 / 590.

**Exit flow**
- `GET /api/exit/lookup/?q=...` -> gate, slot, times, stay, fee + breakdown.
  `q` can be the full vehicle number, **just the last 4+ characters**, or a ticket number (`PK-0001`).
  If two vehicles end the same way the server asks for more characters (400). Not inside -> `NOT_PARKED 404`.
- `POST /api/exit/collect/` `{ q, payment_method: CASH|UPI, gate }`:
  recalculates the fee *now*, saves a `Payment`, sets `exit_time` (slot is free), returns a receipt.
  A paid ticket again -> `ALREADY_PAID 409`.

**Model `Payment`:** one per visit (`OneToOneField`) - this also blocks double payment.
