import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_base.settings')

app = Celery('_base')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-30-seconds': {
        'task': 'tasks_management.tasks.change_tasks',
        'schedule': 30,

    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()



