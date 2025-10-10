import os
import threading
import traceback
from django.core.mail import send_mail
from django.conf import settings

try:
    import requests
except ImportError:
    requests = None  # WhatsApp notifications become optional


def send_async_email(subject, message, recipients):
    """
    Run send_mail() in a background thread to avoid blocking API responses.
    """
    def _send():
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False,
            )
            print(f"✅ Email sent successfully to {recipients}")
        except Exception:
            print("⚠️ Email send failed:")
            traceback.print_exc()

    threading.Thread(target=_send).start()


def notify_reservation_created(reservation):
    """
    Send both email and (optional) WhatsApp notifications when a reservation is created.
    """

    # ----- 1. Admin email notification -----
    subject_admin = f"New Reservation: {reservation.guest_name} ({reservation.room.name})"
    message_admin = f"""
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

    send_async_email(subject_admin, message_admin, ["aheebwatim@gmail.com"])

    # ----- 2. Guest confirmation email -----
    subject_guest = "Your 6A Hotel Reservation Request"
    message_guest = f"""
Dear {reservation.guest_name},

Your reservation at 6A Hotel has been received!

Room: {reservation.room.name}
Check-in: {reservation.check_in}
Check-out: {reservation.check_out}

We’ll contact you shortly to confirm.

Thank you,
6A Hotel Team
"""
    send_async_email(subject_guest, message_guest, [reservation.guest_email])

    # ----- 3. WhatsApp notification (optional) -----
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
                        "body": (
                            f"📩 New Reservation\n"
                            f"Guest: {reservation.guest_name}\n"
                            f"Room: {reservation.room.name}\n"
                            f"Check-in: {reservation.check_in}\n"
                            f"Check-out: {reservation.check_out}\n"
                            f"Guests: {reservation.num_guests}"
                        )
                    },
                },
                timeout=10,
            )
            print("✅ WhatsApp notification sent successfully.")
        except Exception:
            print("⚠️ WhatsApp notification failed.")
            traceback.print_exc()
