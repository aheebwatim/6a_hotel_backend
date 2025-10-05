from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Room, Guest, Booking, Staff
from .serializers import RoomSerializer, GuestSerializer, BookingSerializer, StaffSerializer

# Create your views here.
class RoomList(APIView):
    def get(self, request):
        return Response({"rooms": []})

class BookingList(APIView):
    def get(self, request):
        return Response({"bookings": []})

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
