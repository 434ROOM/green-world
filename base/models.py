import os
from django.db import models
from .utility import getVideoUtility

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200, null=True)
    video_file = models.FileField(upload_to="videos/")
    duration = models.TimeField(auto_now=True)
    fps = models.IntegerField(null=True, blank=False)
    frames = models.IntegerField(null=True, blank=False)
    width = models.IntegerField(null=True, blank=False)
    height = models.IntegerField(null=True, blank=False)

    def save(self, *args, **kwargs):
        if not self.title and self.video_file:
            self.title = os.path.splitext(os.path.basename(self.video_file.name))[0]
        super().save(*args, **kwargs)
        if self.video_file:
            self.frames = getVideoUtility.getFrames(self.video_file.path)
            self.fps = getVideoUtility.getFPS(self.video_file.path)
            self.duration = getVideoUtility.getDuration(self.video_file.path)
            self.width, self.height = getVideoUtility.getResolution(self.video_file.path)
            
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

class Audio(models.Model):
    title = models.CharField(max_length=20)
    audio = models.FileField(upload_to='audios/')
    time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.title and self.audio:
            self.title = os.path.splitext(os.path.basename(self.audio.name))[0]

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.audio:
            if os.path.isfile(self.audio.path):
                os.remove(self.audio.path)
        super().delete(*args, **kwargs)
