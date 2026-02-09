@echo off
echo ========================================
echo   INICIANDO FRONTEND - Pipeline GIS
echo ========================================
echo.

cd /d %~dp0frontend

echo Iniciando servidor de desarrollo Vite...
echo.
echo La URL se mostrara a continuacion
echo Normalmente: http://localhost:3000
echo.
echo Presiona Ctrl+C para detener
echo ========================================
echo.

npm run dev
