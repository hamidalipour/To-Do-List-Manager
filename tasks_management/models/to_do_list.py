from django.db import models

from users.models import User


class ToDoList(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __delete__(self, instance):
        for task in instance.task_set.all():
            task.to_do_lists.remove(instance)
            if not task.to_do_lists.exists():
                task.delete()
        return super(self, instance)
