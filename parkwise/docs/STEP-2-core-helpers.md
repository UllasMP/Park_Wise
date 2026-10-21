# Step 2 - Core helpers (`backend/core`)

| File | What it does |
|------|--------------|
| `errors.py` | `ApiError` + one function per fixed error code (INVALID_VEHICLE 422, ALREADY_PARKED 409, LOT_FULL 409, NOT_PARKED 404, ALREADY_PAID 409, other bad input 400) |
| `api.py` | `@json_api("POST")` decorator: checks method, reads JSON, turns `ApiError` into `{ "code", "message" }` |
| `clock.py` | `clock.now()` = real time + a dev-only offset. **Always use it instead of `timezone.now()`** |
| `lock.py` | one lock so two gates can never grab the same slot |
| `vehicle.py` | clean (`ka 01 ab 1234` -> `KA01AB1234`) and validate (6-10 letters/digits) |
| `seed.py` | clears all visits/payments and creates the 40 slots. **The lot starts empty** (no demo vehicles); `python manage.py seed_data` runs it |
| `views.py` | dev endpoints: `GET/POST /api/dev/clock/`, `POST /api/dev/reset/` = "Clear all data" (only when `DEBUG=True`) |

**Try it:** `curl -X POST localhost:8000/api/dev/clock/ -d '{"minutes": 60}'`
