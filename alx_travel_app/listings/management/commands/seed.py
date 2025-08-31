"""A seeding script to populate the database with a single row of data."""
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from listings.models import Status, Listing, Booking, Review
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        # create an instance of Listing
        listing = Listing.objects.create(
            name='Felix_home', description='A spacious 3 bedroom apartment',
            location='Lagos Nigeria',
            price_per_night=1000.00
            )
        # create an instance of Booking
        booking = Booking.objects.create(
            listing=listing, start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=5),
            total_price=1000.00,
            status='Confirmed',
            )
        # create an instance of Review
        reviews = Review.objects.create(
            listing=listing, rating=4,
            comment='It is cozzy'
            )