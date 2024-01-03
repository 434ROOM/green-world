import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import platform, pathlib
from pathlib import PureWindowsPath, PurePosixPath

def generate_grayscale(photo):
    # Generate and save grayscale image
    if photo:
        original_image_path = photo.path
        img = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plt.figure()
        plt.hist(grayscale_image.ravel(), bins=256, range=[0, 256])
        plt.xlabel('Pixel value')
        plt.ylabel('Number of pixels')
        plt.title('Grayscale histogram')
        plt.savefig(get_image_path(photo, "grayscale"))

        return get_image_url(photo, "grayscale")

def generate_normalization(photo):
    if photo:
        original_image_path = photo.path
        original_image = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        normalized_image = cv2.normalize(original_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        plt.figure()
        plt.hist(normalized_image.ravel(), bins=20)
        plt.Normalize(0, 1)
        plt.title('Normalized histogram')
        plt.savefig(get_image_path(photo, "normalization"))
        
        return get_image_url(photo, "normalization")
    
def generate_gray_processed(photo):
    if photo:
        original_image_path = photo.path
        img = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imencode('.jpg', grayscale_image)[1].tofile(get_image_path(photo, "gray"))

        return get_image_url(photo, "gray")
    
def generate_normalized_processed(photo):
    if photo:
        original_image_path = photo.path
        img = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        normalized_image = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        cv2.imencode('.jpg', normalized_image)[1].tofile(get_image_path(photo, "normalized"))

        return get_image_url(photo, "normalized")

def getUtility(photo):
    if photo:
        original_image_path = photo.path
        image = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        return image.shape[:2]


def get_image_path(photo, folder):
    base_name = os.path.splitext(os.path.basename(photo.name))[0]
    base_dir = os.path.dirname(photo.path)

    image_path = os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    if platform.system().lower() == 'windows':
        return PureWindowsPath(image_path)
    return PurePosixPath(image_path)

def get_image_url(photo, folder):
    base_name = os.path.splitext(os.path.basename(photo.name))[0]
    return os.path.join(f"images/{folder}", f"{base_name}_{folder}.jpg")