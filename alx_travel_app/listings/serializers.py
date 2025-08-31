from rest_framework import serializers
from .models import Listing, Booking, Payment

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'listing_id']

class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at', 'booking_id']

class PaymentSerializer(serializers.model):
    book = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    class Meta:
        model = Payment
        fields = '__all__'