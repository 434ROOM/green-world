from django.shortcuts import render, redirect
from .models import Video, Image
from .forms import VideoForm, ImageForm

# Create your views here.
def home(request):
    return render(request, "base/home.html", {}) 

def videoShow(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.save()
            return redirect("video")
    else:
        form = VideoForm()

    videos = Video.objects.all()
    context = {'form' : form, "videos" : videos}
    return render(request, 'base/video-show.html', context)

def deleteVideo(request, pk):
    video = Video.objects.get(id=pk)

    if request.method == 'POST':
        video.delete()
        return redirect("video")
    return render(request, "base/delete.html", {"obj":video})

def imageShow(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("image")
    else:
        form = ImageForm()

    imgs = Image.objects.all()
    context = {'imgs':imgs, "form": form }
    return render(request, "base/img-show.html", context)

def deleteImg(request, pk):
    img = Image.objects.get(id=pk)

    if request.method == 'POST':
        img.delete()
        return redirect('image')
    return render(request, 'base/delete.html', {"obj":img})