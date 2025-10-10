from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.utils import timezone
import json
import traceback

from .models import Room, Reservation
from .utils.notifications import notify_reservation_created


def _room_is_free(room, start_date, end_date):
    """
    Check if a room is available (no overlapping confirmed/pending reservations).
    """
    conflicts = Reservation.objects.filter(
        room=room,
        status__in=[Reservation.Status.PENDING, Reservation.Status.CONFIRMED]
    ).filter(check_in__lt=end_date, check_out__gt=start_date)
    return not conflicts.exists()


@csrf_exempt
@require_POST
@transaction.atomic
def create_reservation(request):
    """
    Handles creation of a reservation.

    Accepts JSON like:
    {
        "room_id": 1,
        "guest_name": "John Doe",
        "guest_email": "john@example.com",
        "guest_phone": "+256700000000",
        "num_guests": 2,
        "check_in": "2025-10-15",
        "check_out": "2025-10-18",
        "special_requests": "Late check-in"
    }

    or alternatively:
    {
        "room_type": "Single Standard",
        ...
    }
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))

        # Accept either room_id or room_type/name
        room_ref = payload.get("room_id") or payload.get("room_type")
        if not room_ref:
            raise ValidationError("Missing room reference (room_id or room_type).")

        # Resolve room by ID or by name
        try:
            if str(room_ref).isdigit():
                room = Room.objects.get(id=int(room_ref))
            else:
                room = Room.objects.get(name__iexact=str(room_ref).strip())
        except Room.DoesNotExist:
            raise ValidationError(f"Room not found: {room_ref}")

        # Extract guest details
        guest_name = (payload.get("guest_name") or "").strip()
        guest_email = (payload.get("guest_email") or "").strip()
        guest_phone = (payload.get("guest_phone") or "").strip()
        num_guests = int(payload.get("num_guests") or 1)
        check_in = parse_date(payload.get("check_in"))
        check_out = parse_date(payload.get("check_out"))
        special_requests = (payload.get("special_requests") or "").strip()

        # Validate required fields
        if not all([guest_name, guest_email, guest_phone, check_in, check_out]):
            raise ValidationError("Missing required fields (name, email, phone, or dates).")

        if num_guests < 1 or num_guests > room.capacity:
            raise ValidationError("Number of guests exceeds room capacity.")

        if check_out <= check_in:
            raise ValidationError("Check-out must be after check-in.")

        if check_in < timezone.localdate():
            raise ValidationError("Check-in date cannot be in the past.")

        if not _room_is_free(room, check_in, check_out):
            raise ValidationError("Room is not available for the selected dates.")

        # Create reservation record
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

        # Try to send notifications (email / WhatsApp) — fail silently if config missing
        try:
            notify_reservation_created(reservation)
        except Exception as notify_error:
            print("⚠️ Notification error:", notify_error)

        # Success response
        return JsonResponse({
            "ok": True,
            "message": "Reservation created successfully.",
            "confirmation_code": getattr(reservation, "confirmation_code", None),
            "reservation_id": reservation.id,
        }, status=201)

    except ValidationError as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

    except Exception as e:
        # Print traceback for easier debugging (in Render logs)
        traceback.print_exc()
        return JsonResponse({"ok": False, "error": f"Server error: {e}"}, status=500)
