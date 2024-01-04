import os, shortuuid
from django.db import models
from .utility import getVideoUtility, getAudioUtility, getImageUtility
import matplotlib
matplotlib.use('Agg')
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):

    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


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
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
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
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="images/", storage=UUIDStorage)
    width = models.IntegerField(null=True, blank=False)
    height = models.IntegerField(null=True, blank=False)
    grayscale = models.ImageField(upload_to="images/grayscale/", blank=True, null=True, storage=UUIDStorage)
    normalization = models.ImageField(upload_to="images/normalization/", blank=True, null=True, storage=UUIDStorage)
    grayscaleProcessed = models.ImageField(upload_to="images/gray/", blank=True, null=True, storage=UUIDStorage)
    normalizationProcessed = models.ImageField(upload_to="images/normalized/", null=True, blank=True, storage=UUIDStorage)

    objects = ImageQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.title and self.photo:
            self.title = os.path.splitext(os.path.basename(self.photo.name))[0]

        if self.photo and not self.grayscale:
            self.grayscale.name = getImageUtility.generate_grayscale(self.photo)

        if self.photo and not self.normalization:
            self.normalization.name = getImageUtility.generate_normalization(self.photo)

        if self.photo and not self.grayscaleProcessed:
            self.grayscaleProcessed.name = getImageUtility.generate_gray_processed(self.photo)

        if self.photo and not self.normalizationProcessed:
            self.normalizationProcessed.name = getImageUtility.generate_normalized_processed(self.photo)

        self.width, self.height = getImageUtility.getUtility(self.photo)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_image(self.photo)
        self.delete_image(self.grayscale)
        self.delete_image(self.normalization)
        self.delete_image(self.grayscaleProcessed)
        self.delete_image(self.normalizationProcessed)

        super().delete(*args, **kwargs)

    def delete_image(self, field):
        if field:
            file_path = field.path
            if os.path.isfile(file_path):
                os.remove(file_path)

class AudioQuerySet(models.QuerySet):
    def delete(self):
        for audio in self:
            audio.delete_audio()
        super().delete()

class Audio(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
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