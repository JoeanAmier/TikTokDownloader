@echo off
setlocal
set "HERE=%~dp0"
set "PYW=%HERE%douyin_downloader.pyw"
set "VENV=%LOCALAPPDATA%\douk-downloader-venv"
set "VPY=%VENV%\Scripts\python.exe"
set "VPYW=%VENV%\Scripts\pythonw.exe"

if exist "%VPYW%" goto run
echo First run: creating venv and installing dependencies, please wait...
py -3.12 -m venv "%VENV%" 2>nul
if not exist "%VPY%" python -m venv "%VENV%"
if not exist "%VPY%" goto nopython
"%VPY%" -m pip install --upgrade pip
"%VPY%" -m pip install -r "%HERE%requirements.txt"
if errorlevel 1 goto piperr

:run
start "douyin" "%VPYW%" "%PYW%"
goto end

:piperr
echo [ERROR] Dependency install failed. Check network and retry.
pause
goto end

:nopython
echo [ERROR] Python 3.12 not found. Install from python.org then retry.
pause

:end
