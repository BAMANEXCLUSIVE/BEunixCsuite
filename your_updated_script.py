import yt_dlp as youtube_dl
import moviepy.editor as mp
import cv2
import numpy as np
import os
import sys

# Add the Mask_RCNN directory to the system path
sys.path.append(os.path.join(os.getcwd(), "Mask_RCNN"))

from mrcnn import utils
from mrcnn import visualize
import mrcnn.model as modellib
from mrcnn.config import Config

# Directory to save logs and trained model
MODEL_DIR = os.path.join(os.getcwd(), "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(os.getcwd(), "Mask_RCNN/mask_rcnn_coco.h5")

# Ensure the pretrained model is available
if not os.path.exists(COCO_MODEL_PATH):
    raise FileNotFoundError(f"{COCO_MODEL_PATH} not found. Please download it from the appropriate source.")

# Define the configuration for the inference
class InferenceConfig(Config):
    NAME = "coco"
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 80  # COCO dataset has 80 classes + background
    DETECTION_MIN_CONFIDENCE = 0.7

config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(COCO_MODEL_PATH, by_name=True)

def download_video(url, output_path):
    print(f"Downloading video from {url} to {output_path}")
    ydl_opts = {
        'outtmpl': output_path,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Downloaded video to {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def process_video(input_path, output_path):
    print(f"Processing video from {input_path} to {output_path}")
    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        print(f"Error: Downloaded video file {input_path} is missing or empty.")
        return
    
    video = mp.VideoFileClip(input_path)
    processed_video = video.fx(mp.vfx.colorx, 1.0)  # Simple processing
    processed_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    print(f"Saved processed video to {output_path}")

def apply_mask_rcnn(input_path, output_path):
    print(f"Applying Mask R-CNN to video from {input_path} to {output_path}")
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model.detect([frame], verbose=1)
        r = results[0]
        masked_frame = visualize.display_instances(frame, r['rois'], r['masks'], r['class_ids'], 
                                                    ['BG'] + list(range(80)), r['scores'], show_bbox=False, show_mask=True)
        out.write(masked_frame)

    cap.release()
    out.release()
    print(f"Saved Mask R-CNN segmented video to {output_path}")

# Example URLs and paths
urls = [
    'https://www.tiktok.com/@rowanrowofficial/video/7225539309179358470?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7195907683545894149?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7246002609012673797?lang=en&q=men%20fashion%20trend%202025&t=1730850160764'
]

output_dir = 'C:\\Users\\user\\Documents\\BE_Experience_Workplace\\Output TikTok Clone'
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory: {output_dir}")

# Paths for downloaded, processed, and segmented videos
output_paths = [os.path.join(output_dir, f'video{i+1}.mp4') for i in range(len(urls))]
processed_paths = [os.path.join(output_dir, f'processed_video{i+1}.mp4') for i in range(len(urls))]
segmented_paths = [os.path.join(output_dir, f'segmented_video{i+1}.mp4') for i in range(len(urls))]

# Full processing for each video
for url, output_path, processed_path, segmented_path in zip(urls, output_paths, processed_paths, segmented_paths):
    download_video(url, output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"Successfully downloaded video: {output_path}")
        process_video(output_path, processed_path)
        if os.path.exists(processed_path) and os.path.getsize(processed_path) > 0:
            print(f"Successfully processed video: {processed_path}")
            apply_mask_rcnn(processed_path, segmented_path)
            if os.path.exists(segmented_path) and os.path.getsize(segmented_path) > 0:
                print(f"Successfully applied Mask R-CNN to video: {segmented_path}")
            else:
                print(f"Failed to apply Mask R-CNN to video: {segmented_path}")
        else:
            print(f"Failed to process video: {processed_path}")
    else:
        print(f"Failed to download video: {output_path}")
