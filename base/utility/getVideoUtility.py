import cv2
import datetime
"""
# import cv2 
# import datetime 
  
# # create video capture object 
# data = cv2.VideoCapture('C:/Users/Asus/Documents/videoDuration.mp4') 
  
# # count the number of frames 
# frames = data.get(cv2.CAP_PROP_FRAME_COUNT) 
# fps = data.get(cv2.CAP_PROP_FPS) 
  
# calculate duration of the video 
# seconds = round(frames / fps) 
# video_time = datetime.timedelta(seconds=seconds) 
# print(f"duration in seconds: {seconds}") 
# print(f"video time: {video_time}") 
"""

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
