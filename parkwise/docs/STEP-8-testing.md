# Step 8 - Testing

```
cd backend
python manage.py test
```
- `billing/tests.py` - all worked examples (60, 61, 180, 181, 320, 1560 minutes) for 2W and 4W.
- `tickets/tests.py` - every test starts with an empty lot: first slot/ticket, two gates, overflow not allowed,
  LOT_FULL, ALREADY_PARKED, INVALID_VEHICLE, exit, last-4-digit search, ALREADY_PAID, dashboard total,
  block/unblock.

**Manual checks in the UI:** use the dev bar at the bottom: `+1 hour`, `+1 day`, `Clear all data`.
