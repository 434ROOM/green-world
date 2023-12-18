from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("video/", views.videoShow, name="video"),
    path("image/", views.imageShow, name="image"),
    path("delete-video/<str:pk>", views.deleteVideo, name="delete-video"),
    path('delete-image/<str:pk>', views.deleteImg, name="delete-img")
]

