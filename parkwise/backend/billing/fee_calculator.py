"""Pure fee maths (no database) so it is easy to test.

PRICING (change the numbers in RATES / EXTRA_DAY_FEE below if the rules change):

  Bike (2W): Rs30 for the first 2 hours   | then Rs10 for every extra hour
  Car  (4W): Rs50 for the first 2 hours   | then Rs20 for every extra hour
  (a part of an hour counts as a full hour)

  After 24 hours: Rs50 (bike and car) for every extra 24 hours.
  So the first 24 hours use the normal price above, and each further
  24-hour block (or part of one) adds a flat Rs50.

All numbers are whole rupees, so we only use integer maths.
"""
import math

RATES = {
    "2W": {"base": 30, "hourly": 10},
    "4W": {"base": 50, "hourly": 20},
}
BASE_MINUTES = 120        # the base price covers up to 2 hours
MINUTES_PER_DAY = 1440    # 24 hours
EXTRA_DAY_FEE = 50        # per extra 24 hours, same for bike and car


def stay_minutes(entry_time, exit_time):
    """Whole minutes between entry and exit, rounding any extra seconds up."""
    seconds = (exit_time - entry_time).total_seconds()
    return max(0, math.ceil(seconds / 60))


def ceil_div(a, b):
    """Integer division that rounds up (7, 2 -> 4)."""
    return -(-a // b)


def calculate_fee(vehicle_type, minutes):
    """Return the fee plus a breakdown the screen can show."""
    rate = RATES[vehicle_type]

    # Step 1: the first 24 hours -> base price + extra hours after 2 hours
    first_day_minutes = min(minutes, MINUTES_PER_DAY)
    extra_hours = ceil_div(max(0, first_day_minutes - BASE_MINUTES), 60)
    extra_charge = extra_hours * rate["hourly"]
    first_day_fee = rate["base"] + extra_charge

    # Step 2: every further 24 hours (or part of it) adds a flat fee
    extra_days = max(0, ceil_div(minutes, MINUTES_PER_DAY) - 1)
    day_charge = extra_days * EXTRA_DAY_FEE

    return {
        "stay_minutes": minutes,
        "base": rate["base"],
        "extra_hours": extra_hours,
        "hourly_rate": rate["hourly"],
        "extra_charge": extra_charge,
        "first_day_fee": first_day_fee,
        "extra_days": extra_days,
        "day_fee": EXTRA_DAY_FEE,
        "day_charge": day_charge,
        "fee": first_day_fee + day_charge,
    }
