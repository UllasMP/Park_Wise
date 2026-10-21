from django.urls import path

from . import views

urlpatterns = [
    path("dev/clock/", views.dev_clock),
    path("dev/reset/", views.dev_reset),
]
