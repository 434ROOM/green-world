import cv2, os
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

def get_image_url(video_file_name, folder):
    base_name = os.path.splitext(os.path.basename(video_file_name))[0]
    return os.path.join(f"images/{folder}/", f"{base_name}_{folder}.jpg")

def getCover(video_file_url, video_file_name, frames):
    data = cv2.VideoCapture(video_file_url)
    frame_number = frames // 2
    data.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = data.read()  
    cv2.imwrite(get_image_url, frame)      

# def get_image_path(self, folder):
#     # Create a unique path for the image based on the folder (grayscale or normalization)
#     base_name = os.path.splitext(os.path.basename(self.photo.name))[0]
#     base_dir = os.path.dirname(self.photo.path)
#     return os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")
    
