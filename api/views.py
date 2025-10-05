from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room, Service, Reservation
from .serializers import RoomSerializer, ServiceSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def contact_message(request):
    name = request.data.get('name', '')
    email = request.data.get('email', '')
    phone = request.data.get('phone', '')
    message = request.data.get('message', '')

    if not message:
        return Response({'error': 'Message content required.'}, status=400)

    # send the email
    subject = f"New message from {name or 'Guest'} (6A Hotel Website)"
    body = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    
    Message:
    {message}
    """
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,      # from
            ['aheebwatim@gmail.com'],       # to
            fail_silently=False,
        )
        return Response({'success': 'Message sent successfully.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def send_alert_email(name, phone, message):
    subject = f"New message from {name} (6A Hotel Site)"
    body = f"Phone: {phone}\n\nMessage:\n{message}"
    send_mail(subject, body, 'aheebwatim@gmail.com', ['aheebwatim@gmail.com'])

# ------------------------------
# Room ViewSet
# ------------------------------
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['available', 'price']  # filter by availability or price
    ordering_fields = ['price', 'name']       # allow ordering by price or name
    search_fields = ['name', 'description']   # search by name or description


# ------------------------------
# Service ViewSet
# ------------------------------
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['price', 'duration_minutes']      # filter by price/duration
    ordering_fields = ['price', 'duration_minutes', 'name']  # order by these fields
    search_fields = ['name', 'description']               # search by name or description


# ------------------------------
# Reservation ViewSet
# ------------------------------
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can POST/PUT/DELETE
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['service', 'reservation_date']
    ordering_fields = ['reservation_date', 'guest_name']
    search_fields = ['guest_name', 'guest_email']
