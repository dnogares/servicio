@echo off
echo ========================================
echo   INICIANDO BACKEND - Pipeline GIS
echo ========================================
echo.

cd /d %~dp0backend

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo Iniciando servidor FastAPI en puerto 8000...
echo.
echo URLs disponibles:
echo   - API:    http://localhost:8000
echo   - Docs:   http://localhost:8000/docs
echo   - Health: http://localhost:8000/health
echo   - Info:   http://localhost:8000/info
echo.
echo Presiona Ctrl+C para detener
echo ========================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
