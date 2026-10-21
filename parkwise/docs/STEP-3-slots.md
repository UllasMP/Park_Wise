# Step 3 - Slots (`backend/slots`)

**Each gate has its own parking area:** Gate A = B01-B12 + C01-C08, Gate B = B01-B12 + C01-C08
(40 slots in total). C08 starts blocked at both gates (see block/unblock below).

**Model `Slot`:** `gate`, `number`, `slot_type` (2W/4W), `level`, `is_blocked`.
`unique_together = (gate, number)` -> "B01" may exist once per gate.

**`find_free_slot(vehicle_type, gate)`**
1. Look only at slots of **this gate** and **the same type**.
2. Skip blocked slots and slots that have a vehicle inside.
3. Return the lowest number. Nothing free -> `None` (entry raises `LOT_FULL`).

**No overflow:** a 2-wheeler only uses 2-wheeler slots, a 4-wheeler only 4-wheeler slots.
If a gate's 2-wheeler slots are full, the answer is `LOT_FULL`.

A slot is "occupied" when a Visit with `exit_time = NULL` points to it (no flag to keep in sync).

**API:** `GET /api/slots/?gate=Gate A` -> counts + every slot of that gate.
Occupied slots include their `ticket` number so the screen can open the ticket on click.

## Block / unblock a slot
`POST /api/slots/block/` `{ gate, number: "C03", blocked: true|false }` -> `set_slot_blocked()`.
- Blocked slots are skipped by `find_free_slot` and are not counted as free.
- A slot with a vehicle inside cannot be blocked (400 with a clear message).
- Runs inside `parking_lock`, so a slot can't be blocked while an entry is choosing it.
- In the UI: tick **Block / unblock slots** above the map, then click a free slot (block) or a blocked slot (unblock).
- "Clear all data" restores the default (only C08 blocked at each gate).
