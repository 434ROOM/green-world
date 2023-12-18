import os
from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200, null=True)
    video_file = models.FileField(upload_to="videos/", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.title and self.video_file:
            self.title = os.path.splitext(os.path.basename(self.video_file.name))[0]

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.video_file:
            if os.path.isfile(self.video_file.path):
                os.remove(self.video_file.path)
        super().delete(*args, **kwargs)

class Image(models.Model):
    title = models.CharField(max_length = 20)
    photo = models.ImageField(upload_to="images/")

    def save(self, *args, **kwargs):
        if not self.title and self.photo:
            self.title = os.path.splitext(os.path.basename(self.photo.name))[0]

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)