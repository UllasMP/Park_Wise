from django.urls import path

from . import views

urlpatterns = [
    path("exit/lookup/", views.exit_lookup),
    path("exit/collect/", views.exit_collect),
]
