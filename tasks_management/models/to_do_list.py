from django.db import models

from users.models import User


class ToDoList(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #ToDo override delete function
