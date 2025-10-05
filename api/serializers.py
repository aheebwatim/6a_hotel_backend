from rest_framework import serializers
from .models import Room, Service, Reservation

# ------------------------------
# Room Serializer
# ------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


# ------------------------------
# Service Serializer
# ------------------------------
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


# ------------------------------
# Reservation Serializer
# ------------------------------
class ReservationSerializer(serializers.ModelSerializer):
    # Optionally, you can include the service slug or name in the response
    service_name = serializers.ReadOnlyField(source="service.name")
    service_slug = serializers.ReadOnlyField(source="service.slug")

    class Meta:
        model = Reservation
        fields = "__all__"
