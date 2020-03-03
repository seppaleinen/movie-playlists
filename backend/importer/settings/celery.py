import os
from celery import Celery

# DON'T FORGET TO CHANGE THIS ACCORDINGLY
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('importer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
