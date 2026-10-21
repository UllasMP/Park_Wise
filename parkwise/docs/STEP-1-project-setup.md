# Step 1 - Project setup

**Goal:** two folders that talk over HTTP.

```
parkwise/
  backend/    Django (API + rules + SQLite)
  frontend/   React (screens only)
  docs/       these step-by-step notes
```

**Backend:** `django-admin`-style layout by hand: `parkwise/` (settings + urls) and one app per feature:
`core`, `slots`, `tickets`, `billing`, `dashboard`.

**Why one app per feature?** Each file has one job, so a new person can find code quickly.
Dependency direction (no circles): `core` <- `slots` <- `tickets` <- `billing` <- `dashboard`.

**Database:** Django's built-in SQLite (`settings.py` -> `DATABASES`). No extra install.

**Frontend:** Vite + React. `vite.config.js` proxies `/api` to Django, so no CORS setup.

**Key rule:** the server is the source of truth. The frontend never calculates prices or picks slots.
