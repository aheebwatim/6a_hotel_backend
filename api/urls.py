from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ServiceViewSet, ReservationViewSet, contact_message

# ------------------------------
# DRF Router
# ------------------------------
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'reservations', ReservationViewSet, basename='reservation')

# ------------------------------
# URL Patterns
# ------------------------------
urlpatterns = [
    path('', include(router.urls)),                # e.g. /api/rooms/
    path('contact/', contact_message, name='contact_message'),  # /api/contact/
]
