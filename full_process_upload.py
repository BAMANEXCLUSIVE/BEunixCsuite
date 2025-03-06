import os  # Ensure this is imported

from functions import (
    create_caption, analyze_comments, download_video,
    process_video, apply_invisible_mask_with_audio_sync_and_overlay, upload_to_tiktok, run_onnx_model
)

# Main execution function integrating ONNX Runtime for model inference (if needed)
if __name__ == "__main__":
    urls = [
        'https://www.tiktok.com/@rowanrowofficial/video/7225539309179358470',
        'https://www.tiktok.com/@moazz_morgan/video/7195907683545894149',
        'https://www.tiktok.com/@moazz_morgan/video/7246002609012673797'
    ]
    
    output_dir = 'C:\\Users\\user\\Documents\\BE_Experience_Workplace\\Output_TikTok_Clone'
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
                apply_invisible_mask_with_audio_sync_and_overlay(
                    processed_path, masked_path,
                    caption=create_caption([]),  # Empty list for hashtags
                    hashtags="#mensfashion",
                    likes=100,  # Placeholder for likes
                    comments=50,  # Placeholder for comments
                    views=1000,  # Placeholder for views
                    engagement=10.0  # Placeholder for engagement percentage
                )

                if os.path.exists(masked_path) and os.path.getsize(masked_path) > 0:
                    print(f"Successfully applied invisible mask with audio to video: {masked_path}")
                    # Example of creating a caption and uploading the video
                    caption = create_caption([])
                    upload_to_tiktok(masked_path, caption)
