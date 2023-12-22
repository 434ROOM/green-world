from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import GetVideoSerializer, GetImageSerializer, AudioSerializer, AddVideoSerializer, AddImageSerializer
from rest_framework.views import APIView
from django.db.models import Q
import datetime
import os

@api_view(['GET','DELETE']) 
def getVideo(request):
    new_dict = {}
    msg = ""
    time = datetime.datetime.now()

    if request.method == 'GET':
        q = request.GET.get('title') if request.GET.get('title') else ""
        id = request.GET.get('id') if request.GET.get('id') else ""

        if id and q:
            videos = Video.objects.filter(
                Q(id=(int)(id)) &
                Q(title=q)
            )
        elif id and not q:
            videos = Video.objects.filter(
                Q(id=(int)(id))
            )
        else:
            videos = Video.objects.filter(
                Q(title__icontains=q)
            )

        code = status.HTTP_200_OK if videos else status.HTTP_400_BAD_REQUEST
        if code == status.HTTP_200_OK:
            msg = "Get target video successfully"
        else: msg = "Unable to acquire the target video"
        serializer = GetVideoSerializer(videos, many=True)
        new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})

        return Response(new_dict)
    elif request.method == 'DELETE':
        id = request.GET.get('id') if request.GET.get('id') else ""

        if not id:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Please provide valid id value"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)

        obj = Video.objects.filter(id=(int)(id))
        obj.delete()
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
            new_data.update({"id":new_video.id, "title":video_file_name, "video_file":new_video.video_file.url, "duration":new_video.duration,"frames":new_video.frames, "fps":new_video.fps, "width":new_video.width, "height":new_video.height})

            code = status.HTTP_200_OK
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
        else:
            images = Image.objects.filter(
                Q(title__icontains=q)
            )
        code = status.HTTP_200_OK if images else status.HTTP_400_BAD_REQUEST
        if code == status.HTTP_200_OK:
            msg = "Get target image successfully"
        else: msg = "Unable to acquire the target image"

        serializer = GetImageSerializer(images, many=True)
        new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})
        return Response(new_dict, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        id = request.GET.get('id') if request.GET.get('id') else ""

        if not id:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Please provide valid id value"
            new_dict.update({"code":code, "msg":msg, "time":time, "data":{}})
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)

        obj = Image.objects.filter(id=(int)(id))
        obj.delete()
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
                             "grayscale":new_image.grayscale.url,
                             "normalization":new_image.normalization.url
                            })
            
            code = status.HTTP_200_OK
            msg = "Video Uploaded Successfully"

            new_dict.update({"code":code, "msg":msg, "time":time, "data":new_data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def getAudio(request):
    audios = Audio.objects.all()
    serializer = AudioSerializer(audios, many=True)
    return Response(serializer.data)

class addAudio(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AudioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_dict = {}
            time = serializer.data["time"]
            new_dict.update({"code":status.HTTP_201_CREATED, "msg":"Video Uploaded Successfully", "time":time, "data":serializer.data})
            return Response(new_dict, status=status.HTTP_201_CREATED)