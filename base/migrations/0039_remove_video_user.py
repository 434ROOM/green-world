# Generated by Django 5.0 on 2024-01-03 16:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0038_userdata"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="video",
            name="user",
        ),
    ]
