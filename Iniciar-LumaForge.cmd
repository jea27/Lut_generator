@echo off
cd /d "%~dp0"
if not exist ".venv-mvp\Scripts\python.exe" (
  echo Ejecuta primero la preparacion descrita en docs\MVP_V01_WINDOWS.md
  pause
  exit /b 1
)
if not exist "apps\web\dist\index.html" (
  echo Falta compilar la interfaz. Consulta docs\MVP_V01_WINDOWS.md
  pause
  exit /b 1
)
echo LumaForge local: http://127.0.0.1:8790
echo Abre esa direccion en tu navegador. Ctrl+C para detener.
".venv-mvp\Scripts\python.exe" -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8790 --no-access-log
pause
