@echo off
echo ========================================
echo   JARVIS TEC - Inicio Completo
echo ========================================
echo.
echo Este script abrirá dos ventanas:
echo 1. Backend (FastAPI) en http://localhost:8000
echo 2. Frontend (Web) en http://localhost:3000
echo 3. Navegador automático en http://localhost:3000
echo.
pause

start "Jarvis TEC - Backend" cmd /k run-backend.bat
echo Esperando que el backend inicie...
timeout /t 5 /nobreak >nul
start "Jarvis TEC - Frontend" cmd /k run-frontend.bat

echo.
echo ¡Servidores iniciados!
echo El navegador se abrirá automáticamente en unos segundos...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
