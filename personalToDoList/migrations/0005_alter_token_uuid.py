# Generated by Django 5.0.7 on 2024-08-04 10:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalToDoList', '0004_rename_link_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
