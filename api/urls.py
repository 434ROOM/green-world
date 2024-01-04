from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('video', views.getVideo),
    path('add-video', views.addVideo.as_view()),
    path('image', views.getImage),
    path('add-image', views.addImage.as_view()),
    path('audio', views.getAudio),
    path('add-audio', views.addAudio.as_view()),
    path('register', views.RegisterView.as_view()),
    path('login', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]