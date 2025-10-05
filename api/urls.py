from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ServiceViewSet, ReservationViewSet
from django.urls import path
from .views import contact_message

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
    path('api/', include(router.urls)),
]
urlpatterns = [
    path('contact/', contact_message, name='contact_message'),
]