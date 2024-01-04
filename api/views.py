import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import GetVideoSerializer, GetImageSerializer, GetAudioSerializer, AddVideoSerializer, AddImageSerializer, AddAudioSerializer, UserSerializer, MyTokenObtainPairSerializer
from rest_framework.views import APIView
from django.db.models import Q
import datetime, os, jwt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            refresh = response.data['refresh']
            access = response.data['access']

            custom_data = {
                'code' : status.HTTP_200_OK,
                'msg' : "User logged in successfully",
                'time' : now,
                'refresh': refresh,
                'access': access,
            }
            response.data = custom_data

        return response


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def getVideo(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""
        auth = (request.headers.get('Authorization'))
        token = AccessToken(auth.split()[1])
        decoded_token = token.payload
        print(decoded_token)

        if id and q:
            videos = Video.objects.filter(
                Q(id=(int)(id)) & 
                Q(title=q)
            )
        elif id and not q:
            videos = Video.objects.filter(
                Q(id=(int)(id))
            )
        elif not id and not q:
            videos = Video.objects.all()
        else:
            videos = Video.objects.filter(
                Q(title__icontains=q)
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
            video = Video.objects.filter(id=(int)(id))

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

    
class addVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddVideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            new_video = serializer.save()
            video_file_name = os.path.splitext(os.path.basename(new_video.video_file.name))[0]
            new_data = {}
            new_data.update({"id":new_video.id,
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
def getImage(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id and q:
            images = Image.objects.filter(
                Q(id=(int)(id)) | 
                Q(title=q)
            )
        elif id and not q:
            images = Image.objects.filter(
                Q(id=(int)(id))
            )
        elif not id and not q:
            images = Image.objects.all()
        else:
            images = Image.objects.filter(
                Q(title__icontains=q)
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
            img = Image.objects.filter(id=(int)(id))
    
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
            new_image = serializer.save()
            new_data = {}
            new_data.update({"id":new_image.id,
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

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id and q:
            audios = Audio.objects.filter(
                Q(id=(int)(id)) | 
                Q(title=q)
            )
        elif id and not q:
            audios = Audio.objects.filter(
                Q(id=(int)(id))
            )
        elif not id and not q:
            audios = Audio.objects.all()
        else:
            audios = Audio.objects.filter(
                Q(title__icontains=q)
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
            audio = Audio.objects.filter(id=(int)(id))

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
                new_audio = serializer.save()
                new_data = {}
                new_data.update({"id":new_audio.id,
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