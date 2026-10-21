# Step 6 - Dashboard (`backend/dashboard`)

`GET /api/dashboard/` returns:
- `free_slots` - same helper as the slot map (blocked not counted)
- `total_collected_today` - sum of payments whose date is today (uses `clock.now()`, so the dev clock works)
- `exits_today` - receipts, newest first (ticket, vehicle, stay, amount, method)
