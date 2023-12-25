from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from base.models import Video, Image, Audio
from .serializers import GetVideoSerializer, GetImageSerializer, GetAudioSerializer, AddVideoSerializer, AddImageSerializer, AddAudioSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
import datetime, os, cv2, platform
import matplotlib.pyplot as plt
import numpy as np
from pathlib import PureWindowsPath, Path

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
                Q(id=(int)(id)) | 
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
                             "grayscale":new_image.grayscale.url,
                             "normalization":new_image.normalization.url
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
        

class ImageScatterPlotView(View):
    unified_path, unified_url = "", ""
    resolution_base_name = "resolution_plot"
    size_base_name = "size_plot"
    color_base_name = "color_plot"
    folder = "plots"

    def get_scatter_plot_url(self, name):
        url = Path(self.unified_url) / self.folder / f"{name}.png"
        if platform.system().lower() == 'windows':
            return PureWindowsPath(url)
        return url
    
    def get_scatter_plot_path(self, name):
        path = Path(self.unified_path) / f"{name}.png"
        if platform.system().lower() == 'windows':
            return PureWindowsPath(path)
        return path

    def generate_scatter_plots(self, images):
        resolutions = []
        sizes = []
        color_distributions = []

        for image in images:
            img = cv2.imdecode(np.fromfile(image.photo.path, dtype=np.uint8), -1)
            resolution = img.shape[:2]
            resolutions.append(resolution)
            sizes.append(os.path.getsize(image.photo.path))
            color_distributions.append(np.bincount(img.flatten(), minlength=256))

        resolutions = np.array(resolutions)
        sizes = np.array(sizes)
        color_distributions = np.array(color_distributions)

        resolution_path = self.get_scatter_plot_path(self.resolution_base_name)
        size_path = self.get_scatter_plot_path(self.size_base_name)
        color_path = self.get_scatter_plot_path(self.color_base_name)

        if not os.path.exists(resolution_path):
            plt.scatter(resolutions[:, 0], resolutions[:, 1])
            plt.title("Distribution of Image Resolutions")
            plt.xlabel("Width (pixels)")
            plt.ylabel("Height (pixels)")
            plt.savefig(resolution_path)
            plt.close()

        if not os.path.exists(size_path):
            plt.hist(sizes)
            plt.title("Distribution of Image Sizes")
            plt.xlabel("File Size (bytes)")
            plt.ylabel("Number of Images")
            plt.savefig(size_path)
            plt.close()

        # Generate bar plot for mean color distribution
        mean_color_distribution = np.mean(color_distributions, axis=0)
        if not os.path.exists(color_path):
            plt.bar(np.arange(256), mean_color_distribution)
            plt.title("Mean Color Distribution")
            plt.xlabel("Color Value")
            plt.ylabel("Number of Pixels")
            plt.savefig(color_path)
            plt.close()

        return (
            self.get_scatter_plot_url(self.resolution_base_name),
            self.get_scatter_plot_url(self.size_base_name),
            self.get_scatter_plot_url(self.color_base_name),
        )

    def get(self, request, *args, **kwargs):
        images = Image.objects.all()
        time = datetime.datetime.now()

        if not images:
            code = status.HTTP_204_NO_CONTENT
            msg = "Database is currently empty"
            resolutions_plot_url = ""
            sizes_plot_url = ""
            color_distribution_plot_url = ""

            response_data = {
                "code":code,
                "msg":msg,
                "time":time,
                "resolutions_plot_url": resolutions_plot_url,
                "sizes_plot_url": sizes_plot_url,
                "color_distribution_plot_url": color_distribution_plot_url,
            }

        else:
            code = status.HTTP_201_CREATED
            msg = "Get image utility successfully"
            self.unified_path = os.path.dirname(images[0].photo.path)
            self.unified_url = os.path.dirname(images[0].photo.url)

            scatter_plots_exist = (
                os.path.exists(self.get_scatter_plot_path(self.resolution_base_name))
                and os.path.exists(self.get_scatter_plot_path(self.size_base_name))
                and os.path.exists(self.get_scatter_plot_path(self.color_base_name))
            )

            if not scatter_plots_exist:
                (
                    resolutions_plot_url,
                    sizes_plot_url,
                    color_distribution_plot_url,
                ) = self.generate_scatter_plots(images)
            else:
                resolutions_plot_url = str(self.get_scatter_plot_url(self.resolution_base_name))
                sizes_plot_url = str(self.get_scatter_plot_url(self.size_base_name))
                color_distribution_plot_url = str(self.get_scatter_plot_url(self.color_base_name))
            response_data = {
                "code":code,
                "msg":msg,
                "time":time,
                "resolutions_plot_url": resolutions_plot_url,
                "sizes_plot_url": sizes_plot_url,
                "color_distribution_plot_url": color_distribution_plot_url,
            }

        return JsonResponse(response_data)

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