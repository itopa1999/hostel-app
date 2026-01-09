import os
from celery import Celery
from celery.schedules import crontab

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.dev')

app = Celery('hostel')

# Load configuration from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
