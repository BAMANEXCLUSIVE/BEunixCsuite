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
echo.

:: Navigate to the Project Directory
cd C:\Users\user\Documents\BE_Experience_Workplace

:: Create Output Directory if it doesn't exist
IF NOT EXIST "C:\Users\user\Documents\BE_Experience_Workplace\Output TikTok Clone" (
    mkdir "C:\Users\user\Documents\BE_Experience_Workplace\Output TikTok Clone"
)

:: Run the Python Script
python download_process_upload.py
echo.

:: Pause the script to see the results
pause
