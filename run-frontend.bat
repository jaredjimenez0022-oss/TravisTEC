@echo off
echo ========================================
echo   JARVIS TEC - Frontend Server
echo ========================================
echo.
echo Instalando dependencias...
cd frontend

if not exist node_modules (
    npm install
)

echo.
echo Iniciando servidor frontend...
echo Frontend URL: http://localhost:3000
echo.
echo Abriendo navegador en 3 segundos...
timeout /t 3 /nobreak >nul
start http://localhost:3000
npm run dev
