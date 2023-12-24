from django.urls import path
from . import views

urlpatterns = [
    path('video', views.getVideo),
    path('add-video', views.addVideo.as_view()),
    path('image', views.getImage),
    path('image/utility', views.ImageScatterPlotView.as_view()),
    path('add-image', views.addImage.as_view()),
    path('audio', views.getAudio),
    path('add-audio', views.addAudio.as_view())
]