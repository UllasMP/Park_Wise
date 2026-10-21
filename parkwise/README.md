# ParkWise - Parking Management (React + Django)

Three screens: **Entry**, **Exit & payment**, **Dashboard**.
The Django backend owns every rule; the React frontend only shows what the server returns.

## Run it

**Backend** (Python 3.10+):
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data      # creates 40 slots (20 per gate); the lot starts empty
python manage.py runserver      # http://127.0.0.1:8000
```

**Frontend** (Node 18+), in a second terminal:
```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

**Tests:** `cd backend && python manage.py test`

## Tech
React 18 + Vite, `useContext` for state (no Redux) - Django (no DRF) - built-in SQLite.

## Folders
```
backend/  parkwise (settings) | core | slots | tickets | billing | dashboard
frontend/ src/api | context | components | pages
docs/     STEP-1 ... STEP-9 notes explaining how each part was built
```

## API
| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/api/slots/?gate=Gate A` | that gate's slot map + free counts |
| POST | `/api/slots/block/` | block / unblock a slot |
| POST | `/api/entry/` | issue ticket |
| GET | `/api/exit/lookup/?q=` | stay + fee preview |
| POST | `/api/exit/collect/` | pay, release slot, receipt |
| GET | `/api/dashboard/?gate=Gate A` | free slots, today's money, today's exits |
| GET/POST | `/api/dev/clock/` | dev only: move server clock forward |
| POST | `/api/dev/reset/` | dev only: clear all data |

Errors: `{ "code": "...", "message": "..." }` - INVALID_VEHICLE 422, ALREADY_PARKED 409,
LOT_FULL 409, NOT_PARKED 404, ALREADY_PAID 409, any other bad input 400.

## Assumptions
- Each gate has its own 12 + 8 slots. A 2-wheeler only uses 2-wheeler slots (no overflow); a full type gives LOT_FULL.
- Click a black (occupied) slot to see its ticket. Any gate can collect payment for any ticket.
- Vehicle type values are `2W` / `4W`; the UI shows 2-Wheeler / 4-Wheeler.
- A text containing `PK-` is read as a ticket number, otherwise as a vehicle number.
- Fees: bike Rs30 / car Rs50 for 2 hours, then Rs10 / Rs20 per extra hour (part of an hour = full hour), then Rs50 per extra 24 hours. Edit `billing/fee_calculator.py` to change.
- Exit accepts the last 4+ characters of a vehicle number (asks for more if two match).
- Looking up an already-paid ticket on the Exit screen gives NOT_PARKED; trying to *collect* on it gives ALREADY_PAID.
- The lot starts empty. **Clear all data** in the dev bar (or `python manage.py seed_data`) resets everything.
- Any slot can be blocked/unblocked (not while a vehicle is inside). Only C08 starts blocked at each gate.
- "Today" uses the Asia/Kolkata date and the (possibly moved) server clock.
- The dev clock offset lives in memory and resets when the server restarts.

## What I would improve with more time
Concurrency test with real threads, CSV export, split by vehicle type on the dashboard, lost-ticket charge, keyboard shortcuts.
