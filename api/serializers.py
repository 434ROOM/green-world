import os
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import serializers
from base.models import Video, Image, Audio
from django.core.files.storage import default_storage
from base.utility import getVideoUtility

class GetVideoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Video
        fields = '__all__'

class AddVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_file']

    def to_internal_value(self, data):
        """
        Custom method to process incoming data before validation.
        """
        # Call the parent class's to_internal_value for default behavior
        internal_value = super().to_internal_value(data)

        # Fill in additional fields before validation
        video_file = internal_value.get('video_file')

        if video_file:
            existing_video = Video.objects.filter(video_file=video_file).first()
            if existing_video:
                return existing_video

            saved_video = self.save_video(video_file)
            
            video_url = self.get_absolute_path(saved_video.video_file.name)
            internal_value['duration'] = getVideoUtility.getDuration(video_url)
            internal_value['frames'] = getVideoUtility.getFrames(video_url)
            internal_value['fps'] = getVideoUtility.getFPS(video_url)
            internal_value['width'], internal_value['height'] = getVideoUtility.getResolution(video_url)

        return internal_value
    
    def save_video(self, video_file):
        # return Video.objects.create(video_file=video_file)
        saved_video = Video(video_file=video_file)
        saved_video.save()
        return saved_video
    
    def get_absolute_path(self, relative_path):
        return default_storage.path(relative_path)
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'