import cv2
import datetime

def getResolution(video_file_url):
    data = cv2.VideoCapture(video_file_url)
    return [data.get(cv2.CAP_PROP_FRAME_WIDTH), data.get(cv2.CAP_PROP_FRAME_HEIGHT)]

def getFrames(video_file_url):
    return cv2.VideoCapture(video_file_url).get(cv2.CAP_PROP_FRAME_COUNT)

def getFPS(video_file_url):
    return cv2.VideoCapture(video_file_url).get(cv2.CAP_PROP_FPS)

def getDuration(video_file_url):
    frames = getFrames(video_file_url)
    fps = getFPS(video_file_url)
    return datetime.timedelta(seconds=round(frames/fps))
