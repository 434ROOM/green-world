# Generated by Django 4.2.7 on 2023-12-22 02:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0023_image_grayscale_image_normalization"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="cover",
            field=models.ImageField(blank=True, null=True, upload_to="video/cover/"),
        ),
    ]
