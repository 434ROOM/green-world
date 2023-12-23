import cv2
import os
import numpy as np

def generate_grayscale(photo):
    # Generate and save grayscale image
    if photo:
        original_image_path = photo.path
        img = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayscale_path = get_image_path(photo, "grayscale")
        cv2.imwrite(grayscale_path, grayscale_image)
        return get_image_url(photo, "grayscale")

def generate_normalization(photo):
    if photo:
        original_image_path = photo.path
        original_image = cv2.imdecode(np.fromfile(original_image_path, dtype=np.uint8), -1)
        normalized_image = cv2.normalize(original_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        normalization_path = get_image_path(photo, "normalization")
        cv2.imwrite(normalization_path, normalized_image)
        return get_image_url(photo, "normalization")

def get_image_path(photo, folder):
    # Create a unique path for the image based on the folder (grayscale or normalization)
    base_name = os.path.splitext(os.path.basename(photo.name))[0]
    base_dir = os.path.dirname(photo.path)
    return os.path.join(f"{base_dir}/{folder}/", f"{base_name}_{folder}.jpg")

def get_image_url(photo, folder):
    base_name = os.path.splitext(os.path.basename(photo.name))[0]
    return os.path.join(f"images/{folder}", f"{base_name}_{folder}.jpg")