import cv2
from django.utils import timezone

def getResolution(video_file_url):
    data = cv2.VideoCapture(video_file_url)
    if not data.isOpened:
        return [100, 100]
    return [data.get(cv2.CAP_PROP_FRAME_WIDTH), data.get(cv2.CAP_PROP_FRAME_HEIGHT)]

def getFrames(video_file_url):
    return cv2.VideoCapture(video_file_url).get(cv2.CAP_PROP_FRAME_COUNT)

def getFPS(video_file_url):
    return cv2.VideoCapture(video_file_url).get(cv2.CAP_PROP_FPS)

def getDuration(video_file_url):
    data = cv2.VideoCapture(video_file_url)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    return timezone.timedelta(seconds=round(frames/fps))
