"""All API routes live under /api/. Each app owns its own urls.py."""
from django.urls import include, path

urlpatterns = [
    path("api/", include("slots.urls")),
    path("api/", include("tickets.urls")),
    path("api/", include("billing.urls")),
    path("api/", include("dashboard.urls")),
    path("api/", include("core.urls")),
]
