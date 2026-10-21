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

