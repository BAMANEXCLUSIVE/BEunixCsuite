import os
import shutil

# Define the base directory
base_dir = r'C:\Users\user\Documents\BE_Experience_Workplace'

# Define the TikTokUploader directory and files
tiktok_uploader_dir = os.path.join(base_dir, 'TikTokUploader')
files_to_ensure = [
    os.path.join(tiktok_uploader_dir, 'tiktok.py'),
    os.path.join(tiktok_uploader_dir, '__init__.py'),
]

# Define the test_import.py file
test_import_file = os.path.join(base_dir, 'test_import.py')

# Create TikTokUploader directory if it doesn't exist
if not os.path.exists(tiktok_uploader_dir):
    os.makedirs(tiktok_uploader_dir)

# Create necessary files in TikTokUploader directory if they don't exist
for file in files_to_ensure:
    if not os.path.exists(file):
        open(file, 'w').close()  # This will create an empty file

# Ensure the test_import.py file exists in the base directory
if not os.path.exists(test_import_file):
    with open(test_import_file, 'w') as f:
        f.write('from TikTokUploader.tiktok import upload_video  # Ensure this import works\n\nprint("Import successful!")\n')

print("Directory structure is set up correctly.")
