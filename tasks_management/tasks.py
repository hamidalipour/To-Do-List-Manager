import os

from celery.app import shared_task

from tasks_management.models import Task
from django.utils import timezone
from celery import Celery


@shared_task
def change_tasks():
    Task.objects.filter(due_date__lte=timezone.now()).update(done=True)
    print("tasks are done")
