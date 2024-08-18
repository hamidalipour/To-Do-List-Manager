import uuid

from django.db import models

from tasks_management.models.task import Task


class Token(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid