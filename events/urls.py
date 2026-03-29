from django.urls import path
from . import views

urlpatterns = [
    path("<str:event_id>/", views.api_event_detail),
    path("", views.api_events),
]