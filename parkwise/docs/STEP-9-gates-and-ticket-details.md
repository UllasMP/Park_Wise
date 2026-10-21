# Step 9 - Gates and ticket details (changes after review)

1. **Separate parking area per gate.** The gate picker at the top switches the whole slot map.
   Entry at Gate B only uses Gate B slots (see `find_free_slot`).
2. **No 2-wheeler overflow.** 2-wheelers never go to C slots.
3. **Gate on every ticket.** The ticket, receipt and dashboard show the entry gate
   (`visit.slot.gate`) and the gate where payment was collected (`Payment.gate`).
4. **Click a black slot -> full ticket.** `SlotMap` -> `TicketDetails` pop-up calls
   `GET /api/exit/lookup/?q=<ticket>`: gate, slot, vehicle, entry time, stay so far, fee if paid now.
5. **Extra feature:** the dashboard shows money collected per gate.

Rules kept: a vehicle can be inside only once (across both gates); any gate can collect payment for any ticket.

# Later change: pricing and search by last 4 digits
- New pricing (bike Rs30 / car Rs50 for 2 hours, Rs10 / Rs20 per extra hour, Rs50 per extra 24 hours) - see STEP-5.
- Exit accepts the last 4 characters of the vehicle number (`find_visit` in `tickets/services.py`).

# Later change: empty lot + block/unblock
- Seed data now only creates slots; no demo vehicles. Use **Clear all data** (dev bar) to start fresh.
- Slots can be blocked/unblocked from the slot map (STEP-3).
