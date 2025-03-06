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

:: Download Python 3.10 installer
echo Downloading Python 3.10 installer...
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe"

:: Install Python 3.10
echo Installing Python 3.10...
start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

:: Clean up the installer
del python-3.10.0-amd64.exe

:: Verify Python installation
echo Verifying Python installation...
cmd /c "python --version"

pause
