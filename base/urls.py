from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("video/", views.videoShow, name="video"),
    path("image/", views.imageShow, name="image"),
    path("audio/", views.audioShow, name="audio"),
    path("delete-video/<str:pk>", views.deleteVideo, name="delete-video"),
    path('delete-image/<str:pk>', views.deleteImg, name="delete-img"),
    path('delete-audio/<str:pk>', views.deleteAudio, name="delete-audio")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

