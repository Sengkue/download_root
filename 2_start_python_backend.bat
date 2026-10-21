@echo off
title MeDownloader & Meta MusicGen Python Backend
cd /d "%~dp0backend_python"
echo ============================================================
echo   Starting Python FastAPI Backend (Port 3005) ...
echo   Includes Meta MusicGen AI, Media Editor, Social Sync
echo ============================================================
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    call venv\Scripts\pip.exe install -r requirements.txt
    call venv\Scripts\pip.exe install gradio_client replicate
)
set PYTHONUNBUFFERED=1
call venv\Scripts\python.exe main.py
pause
