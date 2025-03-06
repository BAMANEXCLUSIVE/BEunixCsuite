import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return f"{package} installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Failed to install {package}. Error: {e.output}"

def main():
    packages = [
        "yt-dlp", "moviepy", "opencv-python-headless", "tensorflow", 
        "mrcnn", "keras", "textblob", "requests", "pandas",
        "aiohttp", "frozenlist", "multidict", "orjson", "yarl"
    ]
    
    with open("installation_errors.log", "w") as log_file:
        for package in packages:
            result = install_package(package)
            print(result)
            if "Failed" in result:
                log_file.write(result + "\n")
            log_file.write(result + "\n")

if __name__ == "__main__":
    main()
