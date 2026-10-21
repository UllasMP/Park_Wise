from django.urls import path

from . import views

urlpatterns = [
    path("slots/", views.slot_map_view),
    path("slots/block/", views.slot_block_view),
]
