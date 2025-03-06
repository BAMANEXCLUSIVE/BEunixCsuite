@echo off
:: Check for Administrator Privileges
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
   PUSHD "%~dp0"
   POWERSHELL -Command "Start-Process '%~nx0' -ArgumentList '%*' -Verb RunAs"
   POPD
   EXIT
)

:: Print message to confirm administrator privileges
echo Running as administrator...

:: Set Python Path (ensure this points correctly to your Python installation)
SET PATH=C:\Users\user\AppData\Local\Programs\Python\Python39;C:\Users\user\AppData\Local\Programs\Python\Python39\Scripts;%PATH%

:: Navigate to the Project Directory
cd C:\Users\user\Documents\BE_Experience_Workplace

:: Activate virtual environment (if exists)
IF EXIST "venv\Scripts\activate" (
   echo Activating virtual environment...
   CALL venv\Scripts\activate 
)

:: Install required packages
pip install yt-dlp moviepy opencv-python-headless jax jaxlib chainer onnxruntime httpx aiohttp frozenlist multidict orjson yarl

:: Clone TikTokUploader repository if not already present
IF NOT EXIST "TikTokUploader" (
   git clone https://github.com/546200350/TikTokUploader.git 
)

:: Navigate into TikTokUploader directory
cd TikTokUploader

:: Install TikTokUploader dependencies
pip install -r requirements.txt

:: Navigate back to project directory
cd ..

:: Run the Python Script
python full_process_upload.py 
pause
