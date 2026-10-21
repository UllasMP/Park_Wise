# Step 4 - Entry and tickets (`backend/tickets`)

**Model `Visit`** = one ticket. Fields: vehicle number, type, slot, operator, `entry_time`, `exit_time`.
Visits are **never deleted**; paying only fills `exit_time`.
Ticket number is built from the id: `PK-0001`, `PK-0002`, ...

**Two database constraints** (second safety net): one active visit per slot, one active visit per vehicle.

**`issue_ticket()` order of checks**
1. Operator valid? Fields present? -> else `400`
2. Clean number, 6-10 letters/digits? type is 2W/4W? -> else `INVALID_VEHICLE 422`
3. Inside `parking_lock` + `transaction.atomic()`:
   - vehicle already inside -> `ALREADY_PARKED 409`
   - no slot -> `LOT_FULL 409`
   - else create Visit with `entry_time = clock.now()`

**Why the lock?** Gate A and Gate B may send entries at the same time. The lock makes them run one
after another, so the second one sees the first slot as taken.

**`find_visit(text)`** (used by exit): `PK-0142` = ticket; otherwise the full vehicle number or its last 4+ characters.

**API:** `POST /api/entry/` `{ vehicle_number, vehicle_type: "2W"|"4W", operator }` -> `201` ticket.
