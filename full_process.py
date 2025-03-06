import yt_dlp as youtube_dl
import moviepy.editor as mp
import cv2
import numpy as np
import os
import time

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

def apply_invisible_mask_with_audio_sync(input_path, output_path):
    print(f"Applying invisible mask with audio synchronization to video from {input_path} to {output_path}")
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Load the video with moviepy to retain audio
    video = mp.VideoFileClip(input_path)

    # Create an invisible mask
    ret, frame = cap.read()
    height, width, _ = frame.shape
    mask = np.ones((height, width, 4), dtype=np.uint8) * 255  # Fully white transparent mask

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_output_path = "temp_masked_video.mp4"
    out = cv2.VideoWriter(temp_output_path, fourcc, 20.0, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        combined_frame = cv2.addWeighted(bgr_frame, 1, mask, 0, 0)  # No visible effect but keeps the mask in place
        out.write(cv2.cvtColor(combined_frame, cv2.COLOR_BGRA2BGR))

    cap.release()
    out.release()

    # Combine the masked video with the original audio, ensuring durations are synchronized
    masked_video = mp.VideoFileClip(temp_output_path).set_audio(video.audio)
    duration = min(masked_video.duration, video.duration)
    masked_video = masked_video.subclip(0, duration)
    masked_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Ensure the file is properly closed
    masked_video.close()
    time.sleep(2)

    os.remove(temp_output_path)
    print(f"Saved video with invisible mask and synchronized audio to {output_path}")

# Example URLs and paths
urls = [
    'https://www.tiktok.com/@rowanrowofficial/video/7225539309179358470?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7195907683545894149?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7246002609012673797?lang=en&q=men%20fashion%20trend%202025&t=1730850160764'
]

output_dir = 'C:\\Users\\user\\Documents\\BE_Experience_Workplace\\Output TikTok Clone'
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory: {output_dir}")

# Paths for downloaded, processed, and masked videos
output_paths = [os.path.join(output_dir, f'video{i+1}.mp4') for i in range(len(urls))]
processed_paths = [os.path.join(output_dir, f'processed_video{i+1}.mp4') for i in range(len(urls))]
masked_paths = [os.path.join(output_dir, f'masked_video{i+1}.mp4') for i in range(len(urls))]

# Full processing for each video
for url, output_path, processed_path, masked_path in zip(urls, output_paths, processed_paths, masked_paths):
    download_video(url, output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"Successfully downloaded video: {output_path}")
        process_video(output_path, processed_path)
        if os.path.exists(processed_path) and os.path.getsize(processed_path) > 0:
            print(f"Successfully processed video: {processed_path}")
            apply_invisible_mask_with_audio_sync(processed_path, masked_path)
            if os.path.exists(masked_path) and os.path.getsize(masked_path) > 0:
                print(f"Successfully applied invisible mask with audio to video: {masked_path}")
            else:
                print(f"Failed to apply invisible mask to video: {masked_path}")
        else:
            print(f"Failed to process video: {processed_path}")
    else:
        print(f"Failed to download video: {output_path}")
