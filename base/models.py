import os, cv2, wave, io
from django.db import models
from .utility import getVideoUtility, getAudioUtility
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import spectrogram
from PIL import Image as PILImage
from pathlib import Path


# Create your models here.

class VideoQuerySet(models.QuerySet):
    def delete(self):
        for video in self:
            video.delete_file()
        super().delete()

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    video_file = models.FileField(upload_to="videos/")
    duration = models.DurationField(null=True, blank=False)
    fps = models.IntegerField(null=True, blank=False)
    frames = models.IntegerField(null=True, blank=False)
    width = models.IntegerField(null=True, blank=False)
    height = models.IntegerField(null=True, blank=False)
    cover = models.ImageField(upload_to="videos/cover/", blank=True, null=True)

    objects = VideoQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video_file:
            self.title = os.path.splitext(os.path.basename(self.video_file.name))[0]
            self.frames = getVideoUtility.getFrames(self.video_file.path)
            self.fps = getVideoUtility.getFPS(self.video_file.path)
            self.duration = getVideoUtility.getDuration(self.video_file.path)
            self.width, self.height = getVideoUtility.getResolution(self.video_file.path)
            self.cover.name = getVideoUtility.getCover(self.video_file.path, self.video_file.name)
            
        super().save(*args, **kwargs)

    def delete_file(self):
        if self.video_file:
            if os.path.isfile(self.video_file.path):
                os.remove(self.video_file.path)
        if self.cover:
            if os.path.isfile(self.cover.path):
                os.remove(self.cover.path)

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)

class ImageQuerySet(models.QuerySet):
    def delete(self):
        for img in self:
            img.delete_image(img.photo)
            img.delete_image(img.grayscale)
            img.delete_image(img.normalization)
        super().delete()

class Image(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="images/")
    grayscale = models.ImageField(upload_to="images/grayscale/", blank=True, null=True)
    normalization = models.ImageField(upload_to="images/normalization/", blank=True, null=True)

    objects = ImageQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.title and self.photo:
            self.title = os.path.splitext(os.path.basename(self.photo.name))[0]

        # Generate and save grayscale image
        if self.photo and not self.grayscale:
            self.grayscale.name = self.generate_grayscale()

        # Generate and save normalized image
        if self.photo and not self.normalization:
            self.normalization.name = self.generate_normalization()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete images when the model instance is deleted
        self.delete_image(self.photo)
        self.delete_image(self.grayscale)
        self.delete_image(self.normalization)
        super().delete(*args, **kwargs)

    def delete_image(self, field):
        if field:
            file_path = field.path
            if os.path.isfile(file_path):
                os.remove(file_path)

    def generate_grayscale(self):
        # Generate and save grayscale image
        if self.photo:
            original_image_path = self.photo.path
            original_image = cv2.imread(original_image_path)
            grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            grayscale_path = self.get_image_path("grayscale")
            cv2.imwrite(grayscale_path, grayscale_image)
            return self.get_image_url("grayscale")

    def generate_normalization(self):
        # Generate and save normalized image using OpenCV
        if self.photo:
            original_image_path = self.photo.path
            # Read the image using OpenCV
            original_image = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)
            # Normalize the image
            normalized_image = cv2.normalize(original_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            # Save the normalized image
            normalization_path = self.get_image_path("normalization")
            cv2.imwrite(normalization_path, normalized_image)
            return self.get_image_url("normalization")

    def get_image_path(self, folder):
        # Create a unique path for the image based on the folder (grayscale or normalization)
        base_name = os.path.splitext(os.path.basename(self.photo.name))[0]
        base_dir = os.path.dirname(self.photo.path)

        data_folder = Path(base_dir/folder)
        data_name = Path(base_name/folder)

        return os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")
    
    def get_image_url(self, folder):
        base_name = os.path.splitext(os.path.basename(self.photo.name))[0]
        return os.path.join(f"images/{folder}", f"{base_name}_{folder}.jpg")

class AudioQuerySet(models.QuerySet):
    def delete(self):
        for audio in self:
            audio.delete_audio()
        super().delete()

class Audio(models.Model):
    title = models.CharField(max_length=20)
    audio = models.FileField(upload_to='audios/')
    spectrogram = models.ImageField(upload_to='audios/spectrogram', null=True, blank=True)
    spectrum_diagram = models.ImageField(upload_to='audios/spectrum_diagram', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.title and self.audio:
            self.title = os.path.splitext(os.path.basename(self.audio.name))[0]
        self.spectrogram.name = getAudioUtility.getSpectrogram(self.audio)

        super().save(*args, **kwargs)

    def delete_audio(self):
        if os.path.isfile(self.audio.path):
            os.remove(self.audio.path)
        self.delete_image(self.spectrogram)
        self.delete_image(self.spectrum_diagram)

    def delete_image(self, field):
        if field:
            file_path = field.path
            if os.path.isfile(file_path):
                os.remove(file_path)

    def delete(self, *args, **kwargs):
        self.delete_audio()
        super().delete(*args, **kwargs)