# Generated by Django 4.0.4 on 2022-05-26 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='completed',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
