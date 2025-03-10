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
    success = run_command("pip install torch torchvision torchaudio")
    if success:
        print("PyTorch installed successfully.")
    else:
        print("Failed to install PyTorch.")
    return success

def verify_pytorch():
    print("Verifying PyTorch installation...")
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        return True
    except ImportError:
        print("PyTorch is not installed correctly.")
        return False

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

if __name__ == "__main__":
    if install_pytorch():
        if verify_pytorch():
            if install_packages():
                if setup_tiktok_uploader():
                    print("All stages completed successfully.")
                    # Run your main script or add further steps here...
                else:
                    print("Failed to set up TikTokUploader.")
            else:
                print("Failed to install required packages.")
        else:
            print("Failed to verify PyTorch installation.")
    else:
        print("Failed to install PyTorch.")
