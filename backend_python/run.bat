@echo off
echo ===================================================
echo Starting MeDownloader Python FastAPI Backend (Port 3005)
echo ===================================================
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\pip.exe install -r requirements.txt
)
venv\Scripts\python.exe main.py
pause
