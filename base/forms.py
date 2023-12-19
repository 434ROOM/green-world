from django.forms import ModelForm
from .models import Video, Image, Audio

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['photo']

class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = ['audio']