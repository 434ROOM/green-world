from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import VideoSerializer, ImageSerializer, AudioSerializer
from rest_framework.views import APIView

@api_view(['GET']) 
def getVideo(request):
    videos = Video.objects.all() 
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)

class addVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
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
            return Response(serializer.data)
        
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
            return Response(serializer.data)