"""Project settings. Kept minimal: no admin, no login, no sessions."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-only-secret-key-change-me"
DEBUG = True  # DEBUG=True also enables the dev-only clock endpoints
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# One Django app per feature
INSTALLED_APPS = [
    "core",       # shared helpers: errors, clock, seed data
    "slots",      # parking slots + slot map
    "tickets",    # vehicle entry + tickets (visits)
    "billing",    # fee calculation + exit/payment
    "dashboard",  # dashboard numbers
]

MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "parkwise.urls"

# Django's built-in SQLite database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

TIME_ZONE = "Asia/Kolkata"
USE_TZ = True  # store real timestamps (aware datetimes)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
