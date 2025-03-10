@echo off
echo Ensure running as Administrator

REM Check File Path
cd C:\Windows\System32\detectron2\detectron2\layers\csrc\ROIAlignRotated
if exist ROIAlignRotated_cpu.cpp (
    echo File found: ROIAlignRotated_cpu.cpp
) else (
    echo File not found: Ensure the correct path or download the required files
    pause
    exit /b
)

REM Reinstall detectron2
pip uninstall detectron2 -y
cd C:\Windows\System32\detectron2
pip install -e .

REM Check Permissions
icacls C:\Windows\System32\detectron2 /grant %username%:F /T

REM Set Up Visual Studio Build Tools
"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" amd64

echo Setup completed successfully
pause
