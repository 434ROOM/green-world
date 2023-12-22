from rest_framework import serializers
from base.models import Video, Image, Audio

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
    
class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AddImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']
    
    def save(self, **kwargs):
        instance = Image(**self.validated_data)
        instance.save()
        return instance

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'