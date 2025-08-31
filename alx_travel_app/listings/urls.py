from django.urls import path
from .views import ListingView, BookingView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'listing', ListingView, basename='listing')
router.register(r'booking', BookingView, basename='booking')
app_urlpatterns = router.urls
