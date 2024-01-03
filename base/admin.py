from django.contrib import admin
from .models import Video, Image, Audio, UserData

# Register your models here.
admin.site.register(UserData)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(Audio)