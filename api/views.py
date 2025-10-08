from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

from .models import Room, Reservation
from .utils.notifications import notify_reservation_created

def _room_is_free(room, start_date, end_date):
    # any overlap means not free
    conflicts = Reservation.objects.filter(room=room, status__in=[Reservation.Status.PENDING, Reservation.Status.CONFIRMED]) \
        .filter(check_in__lt=end_date, check_out__gt=start_date)
    return not conflicts.exists()

@csrf_exempt  # if you're using CSRF tokens on frontend, you can remove this
@require_POST
@transaction.atomic
def create_reservation(request):
    """
    Expected JSON:
    {
      "room_id": 1,
      "guest_name": "John Doe",
      "guest_email": "john@example.com",
      "guest_phone": "+2567...",
      "num_guests": 2,
      "check_in": "2025-10-15",
      "check_out": "2025-10-18",
      "special_requests": "Late check-in"
    }
    """
    try:
        import json
        payload = json.loads(request.body.decode("utf-8"))

        room_id = payload.get("room_id")
        room = Room.objects.get(id=room_id)

        guest_name = (payload.get("guest_name") or "").strip()
        guest_email = (payload.get("guest_email") or "").strip()
        guest_phone = (payload.get("guest_phone") or "").strip()
        num_guests = int(payload.get("num_guests") or 1)
        check_in = parse_date(payload.get("check_in"))
        check_out = parse_date(payload.get("check_out"))
        special_requests = payload.get("special_requests", "").strip()

        if not all([room, guest_name, guest_email, guest_phone, check_in, check_out]):
            raise ValidationError("Missing required fields.")

        if num_guests < 1 or num_guests > room.capacity:
            raise ValidationError("Number of guests exceeds room capacity.")

        if check_out <= check_in:
            raise ValidationError("Check-out must be after check-in.")

        # Optional: prevent reservations in the past (based on server date)
        from django.utils import timezone
        if check_in < timezone.localdate():
            raise ValidationError("Check-in date cannot be in the past.")

        if not _room_is_free(room, check_in, check_out):
            raise ValidationError("Room is not available for the selected dates.")

        reservation = Reservation.objects.create(
            room=room,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            num_guests=num_guests,
            check_in=check_in,
            check_out=check_out,
            special_requests=special_requests,
            status=Reservation.Status.PENDING,
        )

        # Fire-and-forget notifications (email + whatsapp if configured)
        notify_reservation_created(reservation)

        return JsonResponse({
            "ok": True,
            "message": "Reservation created.",
            "confirmation_code": reservation.confirmation_code,
            "reservation_id": reservation.id
        }, status=201)

    except Room.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Room not found."}, status=404)
    except ValidationError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)
    except Exception as e:
        # You may log this in production
        return JsonResponse({"ok": False, "error": "Unexpected error."}, status=500)
