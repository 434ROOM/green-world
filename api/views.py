import datetime, os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import GetVideoSerializer, GetImageSerializer, GetAudioSerializer, AddVideoSerializer, AddImageSerializer, AddAudioSerializer, UserSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer, AvatarSerializer
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            refresh = response.data['refresh']
            access = response.data['access']

            custom_data = {
                'code' : status.HTTP_200_OK,
                'msg' : "User logged in successfully",
                'time' : datetime.datetime.now(),
                'refresh': refresh,
                'access': access,
            }
            response.data = custom_data

        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_data = {}
        time = datetime.datetime.now()
        new_data.update({
            "code" : status.HTTP_201_CREATED,
            "msg" : "User registered successfully",
            "time" : time,
            "data" : serializer.data
        })

        return Response(new_data, status.HTTP_201_CREATED)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def getVideo(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    auth = request.headers.get('Authorization')
    decoded_token = AccessToken(auth.split()[1]).payload
    user_id = decoded_token['user_id']

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""
        
        if id and q:
            videos = Video.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id)) & 
                Q(title=q)
            )
        elif id and not q:
            videos = Video.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )
        elif not id and not q:
            videos = Video.objects.filter(
                Q(user__id=user_id)
            )

        if videos:
            code = status.HTTP_200_OK
            msg = "Get target video successfully"
        elif not videos and not q and not id:
            code = status.HTTP_204_NO_CONTENT
            msg = "Database is currently empty"
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Unable to acquire the target video"

        serializer = GetVideoSerializer(videos, many=True)
        new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})

        return Response(new_dict, code)
    elif request.method == 'DELETE':
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id:
            video = Video.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )

        if not id or not video:
            code = status.HTTP_404_NOT_FOUND
            msg = "Please provide valid id value"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_404_NOT_FOUND)
        else:
            video.delete()
            code = status.HTTP_200_OK
            msg = "Video instance successfully deleted"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class addVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddVideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            new_video = serializer.save(request.user)
            new_video.user = request.user
            video_file_name = os.path.splitext(os.path.basename(new_video.video_file.name))[0]
            new_data = {}
            new_data.update({
                "user_id":new_video.user.id,
                "user_name":new_video.user.name,
                "video_id":new_video.id,
                "title":video_file_name,
                "video_file":new_video.video_file.url,
                "duration":new_video.duration,
                "frames":new_video.frames,
                "fps":new_video.fps,
                "width":new_video.width,
                "height":new_video.height,
                "cover":new_video.cover.url
            })

            code = status.HTTP_201_CREATED
            msg = "Video Uploaded Successfully"

            new_dict.update({"code":code, "msg":msg, "time":time, "data":new_data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', "DELETE"])
@permission_classes([IsAuthenticated])
def getImage(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    auth = request.headers.get('Authorization')
    decoded_token = AccessToken(auth.split()[1]).payload
    user_id = decoded_token['user_id']

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id and q:
            images = Image.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id)) & 
                Q(title=q)
            )
        elif id and not q:
            images = Image.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )
        elif not id and not q:
            images = Image.objects.filter(
                Q(user__id=user_id)
            )

        if images:
            code = status.HTTP_200_OK
            msg = "Get target image successfully"
        elif not images and not q and not id:
            code = status.HTTP_204_NO_CONTENT
            msg = "Data base is currently empty"
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Unable to acquire the target image"

        serializer = GetImageSerializer(images, many=True)
        new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})
        return Response(new_dict, status=code)
    
    elif request.method == 'DELETE':
        id = request.GET.get('id') if request.GET.get('id') else ""
        if id:
            img = Image.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )
    
        if not id or not img:
            code = status.HTTP_404_NOT_FOUND
            msg = "Please provide valid id value"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_404_NOT_FOUND)
        else:
            img.delete()
            code = status.HTTP_200_OK
            msg = "Image instance successfully deleted"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_200_OK)

class addImage(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            new_image = serializer.save(request.user)
            new_image.user = request.user

            new_data = {}
            new_data.update({
                "id":new_image.id,
                "user_id":new_image.user.id,
                "title":new_image.title,
                "photo":new_image.photo.url,
                "width":new_image.width,
                "height":new_image.height,
                "grayscale":new_image.grayscale.url,
                "normalization":new_image.normalization.url,
                "grayscaleProcessed":new_image.grayscaleProcessed.url,
                "normalizationProcessed":new_image.normalizationProcessed.url
            })
            
            code = status.HTTP_201_CREATED
            msg = "Image Uploaded Successfully"

            new_dict.update({"code":code, "msg":msg, "time":time, "data":new_data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'DELETE'])
def getAudio(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    auth = request.headers.get('Authorization')
    decoded_token = AccessToken(auth.split()[1]).payload
    user_id = decoded_token['user_id']

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id and q:
            audios = Audio.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id)) & 
                Q(title=q)
            )
        elif id and not q:
            audios = Audio.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )
        elif not id and not q:
            audios = Audio.objects.filter(
                Q(user__id=user_id)
            )

        if audios:
            code = status.HTTP_200_OK
            msg = "Get target audio successfully"
        elif not audios and not q and not id:
            code = status.HTTP_204_NO_CONTENT
            msg = "Data base is currently empty"
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Unable to acquire the target audio"

        serializer = GetAudioSerializer(audios, many=True)
        new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})
        return Response(new_dict, status=code)
    
    elif request.method == 'DELETE':
        id = request.GET.get('id') if request.GET.get('id') else ""
        if id:
            audio = Audio.objects.filter(
                Q(user__id=user_id) &
                Q(id=(int)(id))
            )

        if not id or not audio:
            code = status.HTTP_404_NOT_FOUND
            msg = "Please provide valid id value"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_404_NOT_FOUND)
        else:
            audio.delete()
            code = status.HTTP_200_OK
            msg = "Audio instance successfully deleted"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_200_OK)

class addAudio(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddAudioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            try:
                new_audio = serializer.save(request.user)
                new_audio.user = request.user
                new_data = {}
                new_data.update({
                    "id":new_audio.id,
                    "user_id":new_audio.user.id,
                    "title":new_audio.title,
                    "audio":new_audio.audio.url,
                    "spectrogram":new_audio.spectrogram.url,
                    "spectrum_diagram":new_audio.spectrum_diagram.url
                })
                
                code = status.HTTP_201_CREATED
                msg = "Audio Uploaded Successfully"

                new_dict.update({"code":code, "msg":msg, "time":time, "data":new_data})
                return Response(new_dict, status=status.HTTP_201_CREATED)
            except (RuntimeError, ValueError, TypeError) as e:
                code = status.HTTP_500_INTERNAL_SERVER_ERROR
                msg = f"Upload Error: {e}"

                deprecated = Audio.objects.latest('created')
                deprecated.delete()

                new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
                return Response(new_dict, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userProfile(request):
    auth = request.headers.get('Authorization')
    decoded_token = AccessToken(auth.split()[1]).payload

    user_id = decoded_token['user_id']
    username = decoded_token['username']
    email = decoded_token['email']
    avatar = request.user.avatar.url if request.user.avatar.url else ""
    time = datetime.datetime.now()

    if user_id and username and email:
        data = {
            "user_id" : user_id,
            "username" : username,
            "email" : email,
            "avatar" : avatar
        }
        code = status.HTTP_200_OK
        msg = "Get user profile successfully"

        return Response({
            "code" : code,
            "msg" : msg,
            "time" : time,
            "data" : data
        }, code) 
    else:
        code = status.HTTP_400_BAD_REQUEST
        msg = "Unknown Error"
        return Response({
            "code" : code,
            "msg" : msg,
            "time" : time,
            "data" : {}
        })
    
@permission_classes([IsAuthenticated])
class addAvatar(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AvatarSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            new_data = {}

            user = request.user
            if user.avatar:
                os.remove(user.avatar.path)
            user.avatar = serializer.validated_data['avatar']
            user.save()
            
            new_data.update({
                "user_id" : user.id,
                "username" : user.name,
                "avatar" : user.avatar.url
            })
            
            code = status.HTTP_200_OK
            msg = "Avatar uploaded successfully"

            new_dict.update({"code":code, "msg":msg, "time":time, "data":new_data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)