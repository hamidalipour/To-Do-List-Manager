from django.db import models
import uuid

from personal_to_do_list.models.Task import Task


class Token(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)