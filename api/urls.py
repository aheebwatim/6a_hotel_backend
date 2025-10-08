from django.urls import path
from .views import create_reservation

urlpatterns = [
    # Reservation submission endpoint
    path("reservations/", create_reservation, name="create_reservation"),
]
