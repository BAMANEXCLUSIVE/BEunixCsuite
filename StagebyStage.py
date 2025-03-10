import subprocess
import sys

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def install_pytorch():
    print("Installing PyTorch...")
    success = run_command("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    if success:
        print("PyTorch installed successfully.")
    else:
        print("Failed to install PyTorch.")
    return success

if install_pytorch():
    # Proceed to the next stage if PyTorch installation is successful
    # Add the next steps here...

def verify_pytorch():
    print("Verifying PyTorch installation...")
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        return True
    except ImportError:
        print("PyTorch is not installed correctly.")
        return False

if install_pytorch() and verify_pytorch():
    # Proceed to the next stage if PyTorch installation and verification are successful
    # Add the next steps here...

def install_packages():
    print("Installing required packages...")
    packages = [
        "yt-dlp", "moviepy", "opencv-python-headless", "tensorflow", 
        "mrcnn", "keras", "textblob", "requests", "pandas",
        "aiohttp", "frozenlist", "multidict", "orjson", "yarl"
    ]
    for package in packages:
        success = run_command(f"pip install {package}")
        if not success:
            print(f"Failed to install {package}.")
            return False
    return True

if install_pytorch() and verify_pytorch() and install_packages():
    # Proceed to the next stage if all packages are installed successfully
    # Add the next steps here...

def setup_tiktok_uploader():
    print("Setting up TikTokUploader...")
    clone_command = "git clone https://github.com/546200350/TikTokUploder.git TikTokUploader"
    if not run_command(clone_command):
        print("Failed to clone TikTokUploader repository.")
        return False
    install_command = "pip install -r TikTokUploader/requirements.txt"
    if not run_command(install_command):
        print("Failed to install TikTokUploader dependencies.")
        return False
    return True

if install_pytorch() and verify_pytorch() and install_packages() and setup_tiktok_uploader():
    # Proceed to the next stage if TikTokUploader setup is successful
    # Add the next steps here...
