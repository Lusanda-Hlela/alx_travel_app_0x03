from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(to_email, booking_id):
    """
    Background task to send booking confirmation email
    """
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been successfully created."
    from_email = settings.EMAIL_HOST_USER or "no-reply@example.com"

    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=False,
    )
    return f"Email sent to {to_email} for booking {booking_id}"
