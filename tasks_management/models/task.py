from django.db import models
from django.utils import timezone
from tasks_management.models.to_do_list import ToDoList
from tasks_management.validators import validate_date


class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.TextField(default="", verbose_name="توضیحات")
    done = models.BooleanField(default=False, verbose_name="کار تمام شده است؟")
    due_date = models.DateField(
        default=timezone.now().date(), validators=[validate_date], verbose_name="ددلاین تسک"
    )
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.LOW,
        db_index=True,
        verbose_name="اولویت",
    )
    to_do_lists = models.ManyToManyField(ToDoList)
    file = models.FileField(upload_to="media")

    def __str__(self):
        return self.title
