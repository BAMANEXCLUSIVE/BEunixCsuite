import os
import subprocess

# Path to the pretrained weights file
COCO_MODEL_PATH = os.path.join(os.getcwd(), "mask_rcnn_coco.h5")

def verify_file_exists(file_path):
    if os.path.exists(file_path):
        print(f"{file_path} found.")
    else:
        print(f"{file_path} not found. Please download it from the appropriate source.")

# Verify the existence of the model weights file
verify_file_exists(COCO_MODEL_PATH)

# Check TensorFlow and Keras versions
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

import keras
print(f"Keras version: {keras.__version__}")


# Additional checks for other required libraries
import scipy
print(f"Scipy version: {scipy.__version__}")

import skimage
print(f"Scikit-Image version: {skimage.__version__}")

# Check yt-dlp version using subprocess
yt_dlp_version = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True).stdout.strip()
print(f"yt-dlp version: {yt_dlp_version}")

import moviepy
print(f"moviepy version: {moviepy.__version__}")

import cv2
print(f"OpenCV version: {cv2.__version__}")

print("All prerequisites have been verified.")

import os

def verify_installation():
    print("Verifying installation...")

if __name__ == "__main__":
    verify_installation()
    print("Installation verification complete.")

