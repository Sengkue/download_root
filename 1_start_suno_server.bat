@echo off
title Suno API Server
cd /d "%~dp0suno-api"
echo ============================================================
echo   Starting Suno API Server on http://localhost:3008 ...
echo   Make sure you have pasted your SUNO_COOKIE in suno-api\.env
echo ============================================================
set NODE_TLS_REJECT_UNAUTHORIZED=0
call npm run dev
pause
