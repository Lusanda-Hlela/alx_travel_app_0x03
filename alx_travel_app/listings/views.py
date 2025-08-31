import os
from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.response import Response
from uuid import uuid4()
from dotenv import load_dotenv
import requests

#  seting environment variables
load_dotenv()
CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')
class ListingView(viewsets.ModelViewSet):
    """Manually creating view for Listing model."""
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

class PaymentView(viewsets.ViewSet):
    """
    Implementing a view for the payment integration set using the base ViewSet.
    """
    def create(self, request):
        """Initiates payment for a booked listing."""
        initialize_payment_url = "https://api.chapa.co/v1/transaction/initialize"
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        data = request.data
        booking_id = data.get('id')
        tx_ref = str(uuid4())
        booking = Booking.objects.get(id=booking_id)
        amount = booking.total_price
        payment_payload = {
            "amount": amount,
            "currency": "ETB",
            "tx_ref": tx_ref,
            "customization": {
                "title": f"listing payment for {booking.listing.name}__{booking_id} "
                }
        }
        response_data = requests.post(
            initialize_payment_url, json=payment_payload,
            headers=headers
            )
        if response_data.json().get('status') == 'success':
            payment = Payment.objects.create(
                amount=amount, payment_status='pending',
                booking=booking, transaction_id=tx_ref
            )
            if payment:
                return Response(
                    {
                        'status': 'success',
                        'description': 'intialized payment via chapa',
                        'checkout_url': response_data.json()['data']['checkout_url']
                    }
                )
        return Response(
            {
                'status': 'error',
                'description': 'chapa payment intialization failed'
            }
            )