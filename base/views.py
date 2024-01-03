from django.shortcuts import render, redirect
from .models import Video, Image, Audio
from .forms import VideoForm, ImageForm, AudioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")

    context = {"page" : page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'base/login_register.html', {'form' : form})


def home(request):
    return render(request, "base/home.html", {}) 

@login_required(login_url='login')
def videoShow(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect("video")
    else:
        form = VideoForm()

    videos = Video.objects.filter(user=request.user)
    context = {'form' : form, "videos" : videos}
    return render(request, 'base/video-show.html', context)

@login_required(login_url='login')
def deleteVideo(request, pk):
    video = Video.objects.get(id=pk)

    if request.method == 'POST' and request.user == video.user:
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

def audioShow(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("audio")
    else:
        form = AudioForm()
    
    audios = Audio.objects.all()
    context = {"audios":audios, "form":form}
    return render(request, "base/audio-show.html", context)

def deleteAudio(request, pk):
    audio = Audio.objects.get(id=pk)

    if request.method == 'POST':
        audio.delete()
        return redirect('audio')
    return render(request, 'base/delete.html', {"obj":audio})
