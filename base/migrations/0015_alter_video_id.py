# Generated by Django 4.2.7 on 2023-12-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0014_video_height_video_width"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]