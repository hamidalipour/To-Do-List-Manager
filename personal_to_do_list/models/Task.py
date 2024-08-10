from django.db import models

from personal_to_do_list.models.ToDoList import ToDoList


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    done = models.BooleanField(default=False)
    due_date = models.DateField()
    is_priority = models.BooleanField(default=False)
    to_do_lists = models.ManyToManyField(ToDoList)
