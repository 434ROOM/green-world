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

    def save(self, **kwargs):
        instance = Video(**self.validated_data)
        instance.save()
        return instance
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'