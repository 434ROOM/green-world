import os, cv2
from django.db import models
from .utility import getVideoUtility


# Create your models here.
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    video_file = models.FileField(upload_to="videos/")
    duration = models.DurationField(null=True, blank=False)
    fps = models.IntegerField(null=True, blank=False)
    frames = models.IntegerField(null=True, blank=False)
    width = models.IntegerField(null=True, blank=False)
    height = models.IntegerField(null=True, blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video_file:
            self.title = os.path.splitext(os.path.basename(self.video_file.name))[0]
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
    GrayScale = models.ImageField(upload_to="images/grayscale/", blank=True, null=True)
    Normalization = models.ImageField(upload_to="images/normalization/", blank=True, null=True)

class Image(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="images/")
    grayscale = models.ImageField(upload_to="images/grayscale/", blank=True, null=True)
    normalization = models.ImageField(upload_to="images/normalization/", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.title and self.photo:
            self.title = os.path.splitext(os.path.basename(self.photo.name))[0]

        # Generate and save grayscale image
        if self.photo and not self.grayscale:
            grayscale_path = self.generate_grayscale()
            self.grayscale.name = grayscale_path

        # Generate and save normalized image
        if self.photo and not self.normalization:
            normalization_path = self.generate_normalization()
            self.normalization.name = normalization_path

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete images when the model instance is deleted
        self.delete_image(self.photo)
        self.delete_image(self.grayscale)
        self.delete_image(self.normalization)
        super().delete(*args, **kwargs)

    def delete_image(self, field):
        # Delete the image file if it exists
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
            return grayscale_path

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
            return normalization_path

    def get_image_path(self, folder):
        # Create a unique path for the image based on the folder (grayscale or normalization)
        base_name = os.path.splitext(os.path.basename(self.photo.name))[0]
        base_dir = os.path.dirname(self.photo.path)
        return os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")

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
