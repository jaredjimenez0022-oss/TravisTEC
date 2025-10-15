@echo off
cd /d "%~dp0frontend-react"
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   INICIANDO FRONTEND VITE - TravisTEC                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo   Directorio: %CD%
echo   Puerto:     5173
echo   URL:        http://localhost:5173
echo.
echo ════════════════════════════════════════════════════════════
echo.
npm run dev
