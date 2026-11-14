@echo off
title RezX Modz 24/7 Server & Cloudflare
cd /d "%~dp0"
echo ========================================================
echo    Starting RezX Modz 24/7 Portal & Tunnel
echo ========================================================

start "" /B python -u server.py
timeout /t 2 /nobreak >nul
start "" "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8080
