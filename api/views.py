from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import VideoSerializer, ImageSerializer, AudioSerializer
from rest_framework.views import APIView
from django.db.models import Q
import datetime

@api_view(['GET']) 
def getVideo(request):
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
    time = datetime.datetime.now()
    serializer = VideoSerializer(videos, many=True)
    new_dict = {}
    new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})

    return Response(new_dict)

class addVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        new_dict = {}
        time = datetime.datetime.now()

        if serializer.is_valid():
            serializer.save()
            code = status.HTTP_200_OK
            msg = "Video Uploaded Successfully"

            new_dict.update({"code":code, "msg":msg, "time":time, "data":serializer.data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        else:
            code = status.HTTP_400_BAD_REQUEST
            msg = "Upload failure"
            new_dict = {"code":code, "msg":msg, "time":time, "data":{}}
            return Response(new_dict, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET']) 
def getImage(request):
    imgs = Image.objects.all() 
    serializer = VideoSerializer(imgs, many=True)
    return Response(serializer.data)

class addImage(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_dict = {}
            time = serializer.data["time"]
            new_dict.update({"code":status.HTTP_201_CREATED, "msg":"Video Uploaded Successfully", "time":time, "data":serializer.data})
            return Response(new_dict, status=status.HTTP_201_CREATED)
        
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