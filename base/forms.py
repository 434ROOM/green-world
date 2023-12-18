from django.forms import ModelForm
from .models import Video, Image
from django import forms

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['photo']