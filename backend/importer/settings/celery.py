import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings') # DON'T FORGET TO CHANGE THIS ACCORDINGLY

app = Celery('importer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
