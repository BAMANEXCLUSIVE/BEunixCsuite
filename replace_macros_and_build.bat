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

:: Set the directory to your project folder
cd C:\Users\user\Documents\Projects

:: Find and replace deprecated macros in source code files
for /r %%i in (*.c *.cpp *.h *.hpp) do (
    powershell -Command "(Get-Content -Path '%%i') -replace 'Py_TRASHCAN_SAFE_BEGIN', 'Py_TRASHCAN_BEGIN' | Set-Content -Path '%%i'"
    powershell -Command "(Get-Content -Path '%%i') -replace 'Py_TRASHCAN_SAFE_END', 'Py_TRASHCAN_END' | Set-Content -Path '%%i'"
)

:: Print message to confirm completion
echo Completed macro replacement.

:: Run the build process
cd vcpkg\build
cmake ..
cmake --build .

:: Pause to view any output messages
pause
