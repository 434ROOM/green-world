# Generated by Django 4.2.7 on 2023-12-19 17:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0005_video_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="time",
            field=models.DateField(auto_now=True),
        ),
    ]
