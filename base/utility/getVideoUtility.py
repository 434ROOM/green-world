import cv2, os
from django.utils import timezone

def getResolution(video):
    data = cv2.VideoCapture(video.path)
    return [data.get(cv2.CAP_PROP_FRAME_WIDTH), data.get(cv2.CAP_PROP_FRAME_HEIGHT)]

def getFrames(video):
    return cv2.VideoCapture(video.path).get(cv2.CAP_PROP_FRAME_COUNT)

def getFPS(video):
    return cv2.VideoCapture(video.path).get(cv2.CAP_PROP_FPS)

def getDuration(video):
    data = cv2.VideoCapture(video.path)
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    return timezone.timedelta(seconds=round(frames/fps))

def get_image_path(video_file_path, video_file_name, folder):
    base_name = os.path.splitext(os.path.basename(video_file_name))[0]
    base_dir = os.path.dirname(video_file_path)
    return os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")

def get_image_url(video_file_name, folder):
    base_name = os.path.splitext(os.path.basename(video_file_name))[0]
    return os.path.join(f"videos/{folder}/", f"{base_name}_{folder}.jpg")

def getCover(video):
    data = cv2.VideoCapture(video.path)
    frame_number = 30
    data.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = data.read()  
    cv2.imencode('.jpg', frame)[1].tofile(get_image_path(video.path, video.name, "cover"))
    return get_image_url(video.name, "cover")  
    