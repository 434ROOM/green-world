from rest_framework import serializers
from base.models import Video, Image, Audio, UserData
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework import status
import datetime

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    now = datetime.datetime.now()

    default_error_messages = {
        'no_active_account': {
            'code': status.HTTP_401_UNAUTHORIZED,
            'msg': ('No active account found with the given credentials'),
            'time' : now,
            'data' : {}
        },
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.name
        token['email'] = user.email

        return token

class GetVideoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Video
        fields = '__all__'

class AddVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_file']

    def save(self, user, **kwargs):
        instance = Video(**self.validated_data)
        instance.save(user)
        return instance
    
class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class AddImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']
    
    def save(self, user, **kwargs):
        instance = Image(**self.validated_data)
        instance.save(user)
        return instance

class GetAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

class AddAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['audio']

    def save(self, user, **kwargs):
        instance = Audio(**self.validated_data)
        instance.save(user)
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['avatar']