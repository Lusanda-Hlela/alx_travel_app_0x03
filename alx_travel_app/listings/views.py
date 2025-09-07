import os
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import (
    ListingSerializer,
    BookingSerializer,
)  # add PaymentSerializer if needed
from uuid import uuid4
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")


class ListingView(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()


class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


class PaymentView(viewsets.ViewSet):
    """
    View for handling Chapa payment initialization.
    """

    def create(self, request):
        """Initiates payment for a booked listing."""
        booking_id = request.data.get("id")
        if not booking_id:
            return Response(
                {"status": "error", "description": "Booking ID is required"}, status=400
            )

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"status": "error", "description": "Booking not found"}, status=404
            )

        tx_ref = str(uuid4())
        amount = booking.total_price

        initialize_payment_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

        payment_payload = {
            "amount": str(amount),
            "currency": "ETB",
            "tx_ref": tx_ref,
            "customization": {
                "title": f"Listing payment for {booking.listing.name}__{booking_id}"
            },
            # You’ll probably need these based on Chapa docs
            "return_url": "http://localhost:8000/payment/callback/",
            "email": (
                booking.user.email if hasattr(booking, "user") else "test@example.com"
            ),
        }

        response_data = requests.post(
            initialize_payment_url, json=payment_payload, headers=headers
        )
        response_json = response_data.json()

        if response_json.get("status") == "success":
            payment = Payment.objects.create(
                amount=amount, status="pending", booking=booking, transaction_id=tx_ref
            )
            return Response(
                {
                    "status": "success",
                    "description": "Payment initialized via Chapa",
                    "checkout_url": response_json["data"].get("checkout_url"),
                }
            )

        return Response(
            {
                "status": "error",
                "description": response_json.get(
                    "message", "Chapa payment initialization failed"
                ),
            },
            status=400,
        )
