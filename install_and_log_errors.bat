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

:: Navigate to the Project Directory
cd C:\Users\user\Documents\BE_Experience_Workplace

:: Create the Virtual Environment
python -m venv tf_env

:: Navigate to the Environment's Scripts Directory
cd tf_env\Scripts

:: Activate the Environment
activate

:: Navigate to the Project Directory
cd ..

:: Install required packages and log errors
python install_and_log_errors.py

:: Handle additional problematic packages manually
pip install aiohttp frozenlist multidict orjson yarl

:: Clone the TikTokUploader repository if not already present
IF NOT EXIST "TikTokUploader" (
    git clone https://github.com/546200350/TikTokUploder.git TikTokUploader
)

:: Navigate to the TikTokUploader directory
cd TikTokUploader

:: Install TikTokUploader dependencies
pip install -r requirements.txt

:: Navigate back to the project directory
cd ..

:: Run the Python Script
python full_process_upload.py
pause
