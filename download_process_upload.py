import yt_dlp as youtube_dl
import moviepy.editor as mp
import os

# Function to download videos
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

# Function to process videos
def process_video(input_path, output_path):
    print(f"Processing video from {input_path} to {output_path}")
    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        print(f"Error: Downloaded video file {input_path} is missing or empty.")
        return
    
    video = mp.VideoFileClip(input_path)
    processed_video = video.fx(mp.vfx.colorx, 1.0)  # Simple processing: Adjust brightness
    processed_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    print(f"Saved processed video to {output_path}")

# Example URLs and paths
urls = [
    'https://www.tiktok.com/@rowanrowofficial/video/7225539309179358470?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7195907683545894149?lang=en&q=men%20fashion%20trend%202025&t=1730850160764',
    'https://www.tiktok.com/@moazz_morgan/video/7246002609012673797?lang=en&q=men%20fashion%20trend%202025&t=1730850160764'
]

output_dir = 'C:\\Users\\user\\Documents\\BE_Experience_Workplace\\Output TikTok Clone'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory: {output_dir}")

output_paths = [os.path.join(output_dir, f'video{i+1}.mp4') for i in range(len(urls))]
processed_paths = [os.path.join(output_dir, f'processed_video{i+1}.mp4') for i in range(len(urls))]

# Download and process each video
for url, output_path, processed_path in zip(urls, output_paths, processed_paths):
    download_video(url, output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"Successfully downloaded video: {output_path}")
        process_video(output_path, processed_path)
    else:
        print(f"Failed to download video: {output_path}")
    # Check if processed file exists
    if os.path.exists(processed_path) and os.path.getsize(processed_path) > 0:
        print(f"Successfully processed video: {processed_path}")
    else:
        print(f"Failed to process video: {processed_path}")
