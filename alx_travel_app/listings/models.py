from django.db import models
from django.db.models import Q, CheckConstraint
from uuid import uuid4

# Create your models here.

class Status(models.TextChoices):
    pending = 'pending', 'Pending'
    confirmed = 'confirmed', 'Confirmed'
    canceled = 'canceled', 'Canceled'

class Listing(models.Model):
    property_id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

class Booking(models.Model):
    booking_id = models.UUIDField(default=uuid4, primary_key=True)
    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, related_name='booking', null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    status = models.CharField(max_length=50, null=False, blank=False, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.booking_id}'

class Review(models.Model):
    review_id = models.UUIDField(default=uuid4, primary_key=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(null=False, blank=False)
    comment = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name='rating_check'
            )
        ]
    
    def __str__(self):
        return f'{self.review_id} -- Rating {self.rating}'

class Payment(models.Model):
    booking = models.OneToOneField("Booking", on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("paid", "Paid")])
    created_at = models.DateTimeField(auto_now_add=True)
