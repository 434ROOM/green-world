# Generated by Django 5.0 on 2024-01-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0031_image_grayscaleprocessed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="height",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="image",
            name="width",
            field=models.IntegerField(null=True),
        ),
    ]
