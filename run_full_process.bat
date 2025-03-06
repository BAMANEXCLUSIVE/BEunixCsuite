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

:: Run the Python Script
python full_process.py
pause
