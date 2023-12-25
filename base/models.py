import os, shortuuid
from django.db import models
from .utility import getVideoUtility, getAudioUtility, getImageUtility
import matplotlib
matplotlib.use('Agg')
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.files.storage import FileSystemStorage

# Create your models here.

class UUIDStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        my_uuid = shortuuid.ShortUUID().random(length=7)
        new_name = os.path.splitext(name)[0] + f"_{my_uuid}" + os.path.splitext(name)[1]
        return super().get_available_name(new_name, max_length)

class VideoQuerySet(models.QuerySet):
    def delete(self):
        for video in self:
            video.delete_file()
        super().delete()

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    video_file = models.FileField(upload_to="videos/", storage=UUIDStorage)
    duration = models.DurationField(null=True, blank=False)
    fps = models.IntegerField(null=True, blank=False)
    frames = models.IntegerField(null=True, blank=False)
    width = models.IntegerField(null=True, blank=False)
    height = models.IntegerField(null=True, blank=False)
    cover = models.ImageField(upload_to="videos/cover/", blank=True, null=True, storage=UUIDStorage)

    objects = VideoQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video_file:
            self.title = os.path.splitext(os.path.basename(self.video_file.name))[0]
            self.frames = getVideoUtility.getFrames(self.video_file)
            self.fps = getVideoUtility.getFPS(self.video_file)
            self.duration = getVideoUtility.getDuration(self.video_file)
            self.width, self.height = getVideoUtility.getResolution(self.video_file)
            self.cover.name = getVideoUtility.getCover(self.video_file)
            
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
    photo = models.ImageField(upload_to="images/", storage=UUIDStorage)
    grayscale = models.ImageField(upload_to="images/grayscale/", blank=True, null=True, storage=UUIDStorage)
    normalization = models.ImageField(upload_to="images/normalization/", blank=True, null=True, storage=UUIDStorage)

    objects = ImageQuerySet.as_manager()

    def save(self, *args, **kwargs):
        unified_path = os.path.dirname(self.photo.path)
        existing_scatter_plots = [
            os.path.join(f"{unified_path}scatter_plots", f"{self.title}_resolutions_scatter_plot.png"),
            os.path.join(f"{unified_path}scatter_plots", f"{self.title}_sizes_histogram.png"),
            os.path.join(f"{unified_path}scatter_plots", f"{self.title}_mean_color_distribution_bar_plot.png"),
        ]

        for plot_path in existing_scatter_plots:
            if os.path.exists(plot_path):
                os.remove(plot_path)

        super().save(*args, **kwargs)
        if not self.title and self.photo:
            self.title = os.path.splitext(os.path.basename(self.photo.name))[0]

        if self.photo and not self.grayscale:
            self.grayscale.name = getImageUtility.generate_grayscale(self.photo)

        if self.photo and not self.normalization:
            self.normalization.name = getImageUtility.generate_normalization(self.photo)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_image(self.photo)
        self.delete_image(self.grayscale)
        self.delete_image(self.normalization)
        super().delete(*args, **kwargs)

    
    def delete_scatter_plots(self):
        unified_path = os.path.dirname(self.photo.path)
        resolutions_plot_path = os.path.join(f"{unified_path}scatter_plots", f"{self.title}_resolutions_scatter_plot.png")
        sizes_plot_path = os.path.join(f"{unified_path}scatter_plots", f"{self.title}_sizes_histogram.png")
        color_distribution_plot_path = os.path.join(f"{unified_path}scatter_plots", f"{self.title}_mean_color_distribution_bar_plot.png")

        for plot_path in [resolutions_plot_path, sizes_plot_path, color_distribution_plot_path]:
            if os.path.exists(plot_path):
                os.remove(plot_path)

    def delete_image(self, field):
        if field:
            file_path = field.path
            if os.path.isfile(file_path):
                os.remove(file_path)

@receiver(post_delete, sender=Image)
def delete_scatter_plots(sender, instance, **kwargs):
    instance.delete_scatter_plots()

class AudioQuerySet(models.QuerySet):
    def delete(self):
        for audio in self:
            audio.delete_audio()
        super().delete()

class Audio(models.Model):
    title = models.CharField(max_length=20)
    audio = models.FileField(upload_to='audios/', storage=UUIDStorage)
    spectrogram = models.ImageField(upload_to='audios/spectrogram/', null=True, blank=True, storage=UUIDStorage)
    spectrum_diagram = models.ImageField(upload_to='audios/spectrum_diagram/', null=True, blank=True, storage=UUIDStorage)
    created = models.DateTimeField(auto_now_add=True)

    objects = AudioQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if not self.title and self.audio:
                self.title = os.path.splitext(os.path.basename(self.audio.name))[0]
            self.spectrogram.name = getAudioUtility.getSpectrogram(self.audio)
            self.spectrum_diagram = getAudioUtility.getFrequencySpectrum(self.audio)
            super().save(*args, **kwargs)
        except ValueError or TypeError:
            self.delete()
            raise RuntimeError("Unsupported operation")

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