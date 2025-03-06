import cv2
import numpy as np
import moviepy.editor as mp
import os

def apply_invisible_mask_with_audio_sync_and_overlay(input_path, output_path, caption, hashtags, likes, comments, views, engagement):
    print(f"Applying invisible mask with audio synchronization to video from {input_path} to {output_path}")
    
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return
    
    video = mp.VideoFileClip(input_path)
    
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame from video.")
        cap.release()
        return
    
    height, width, _ = frame.shape
    mask = np.ones((height, width, 4), dtype=np.uint8) * 255  # Fully white transparent mask
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_output_path = "temp_masked_video.mp4"
    
    out = cv2.VideoWriter(temp_output_path, fourcc, 20.0, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        combined_frame = cv2.addWeighted(bgr_frame, 1, mask, 0, 0)  # Apply the mask
        
        out.write(cv2.cvtColor(combined_frame, cv2.COLOR_BGRA2BGR))
    
    cap.release()
    out.release()

    masked_video = mp.VideoFileClip(temp_output_path).set_audio(video.audio)
    
    duration = min(masked_video.duration, video.duration)
    masked_video = masked_video.subclip(0, duration)

    # Overlay text onto the video using OpenCV
    def add_text(clip, text, position, fontsize=24, color=(255, 255, 255)):
        def make_frame(t):
            frame = clip.get_frame(t)
            frame = np.array(frame)  # Convert to NumPy array
            cv2.putText(frame, text, position,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        fontsize / 10,
                        color,
                        2,
                        cv2.LINE_AA)
            return frame
        
        return mp.VideoClip(make_frame, duration=clip.duration).set_audio(clip.audio)

    masked_video = add_text(masked_video, caption, (10, height - 30))
    masked_video = add_text(masked_video, hashtags, (10, 30))
    masked_video = add_text(masked_video, f"Likes: {likes}", (10, 60))
    masked_video = add_text(masked_video, f"Comments: {comments}", (10, 90))
    masked_video = add_text(masked_video, f"Views: {views}", (10, 120))
    masked_video = add_text(masked_video, f"Engagement: {engagement}%", (10, 150))

    masked_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    masked_video.close()
    
    # Clean up temporary files
    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

    print(f"Saved video with invisible mask and synchronized audio to {output_path}")