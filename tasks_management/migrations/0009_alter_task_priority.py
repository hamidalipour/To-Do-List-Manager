# Generated by Django 4.2.15 on 2024-08-13 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks_management", "0008_remove_task_is_priority_task_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.SmallIntegerField(
                choices=[("1", "High"), ("2", "Medium"), ("3", "Low")]
            ),
        ),
    ]
