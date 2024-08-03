from django.db import models
from users.models import User

class ToDoList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    done = models.BooleanField(default=False)
    due_date = models.DateField()
    is_priority = models.BooleanField(default=False)
    toDoList = models.ForeignKey(ToDoList, on_delete=models.CASCADE)