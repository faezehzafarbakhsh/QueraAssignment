# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from . import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QueraPyRate.settings')

# Create a Celery instance and configure it using the settings from Django
celery_app = Celery('QueraPyRate')

broker_connection_retry_on_startup = True
# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# This line tells Celery to use Redis as the message broker.
celery_app.conf.broker_url = 'redis://localhost:6379/0'
celery_app.conf.result_backend = 'redis://localhost:6379/0'

# Use the Django-celery-results backend for storing task results.
celery_app.conf.result_backend = 'django-db'

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
