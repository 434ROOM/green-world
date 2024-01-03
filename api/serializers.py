from rest_framework import serializers
from base.models import Video, Image, Audio, UserData

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

class GetAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

class AddAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['audio']

    def save(self, **kwargs):
        instance = Audio(**self.validated_data)
        instance.save()
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user