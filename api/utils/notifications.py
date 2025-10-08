import os
from django.core.mail import send_mail
from django.conf import settings

try:
    import requests
except ImportError:
    requests = None  # WhatsApp notifications become optional


def notify_reservation_created(reservation):
    """
    Send both email and (optional) WhatsApp notifications when a reservation is created.
    """

    # ----- 1. Email notification -----
    subject = f"New Reservation: {reservation.guest_name} ({reservation.room.name})"
    message = f"""
    A new reservation has been created.

    Guest: {reservation.guest_name}
    Email: {reservation.guest_email}
    Phone: {reservation.guest_phone}
    Room: {reservation.room.name}
    Guests: {reservation.num_guests}
    Check-in: {reservation.check_in}
    Check-out: {reservation.check_out}
    Special Requests: {reservation.special_requests or 'None'}

    Confirmation Code: {reservation.confirmation_code}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["aheebwatim@gmail.com"],
        fail_silently=True,
    )

    # ----- 2. WhatsApp notification (optional) -----
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    whatsapp_number_id = os.getenv("WHATSAPP_NUMBER_ID")
    manager_phone = os.getenv("MANAGER_PHONE")

    if requests and whatsapp_token and whatsapp_number_id and manager_phone:
        try:
            requests.post(
                f"https://graph.facebook.com/v18.0/{whatsapp_number_id}/messages",
                headers={
                    "Authorization": f"Bearer {whatsapp_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": manager_phone,
                    "type": "text",
                    "text": {
                        "body": f"📩 New Reservation\nGuest: {reservation.guest_name}\nRoom: {reservation.room.name}\nCheck-in: {reservation.check_in}\nCheck-out: {reservation.check_out}\nGuests: {reservation.num_guests}"
                    },
                },
                timeout=10,
            )
        except Exception:
            pass  # no crash if WhatsApp fails
