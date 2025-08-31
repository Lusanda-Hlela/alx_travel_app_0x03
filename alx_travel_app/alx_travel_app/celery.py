import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# Load settings from Django settings, using "CELERY_" namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks across all installed apps
app.autodiscover_tasks()
