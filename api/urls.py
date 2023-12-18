from django.urls import path
from . import views

urlpatterns = [
    path('video', views.getVideo),
    path('add-video', views.addVideo.as_view()),
    path('image', views.getImage),
    path('add-image', views.addImage.as_view())
]