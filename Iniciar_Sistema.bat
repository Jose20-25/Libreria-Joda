@echo off
title Libreria JODA - Sistema ERP
color 0A

echo ============================================================
echo    SISTEMA ERP - LIBRERIA JODA
echo ============================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.11 o superior
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

echo Iniciando servidor Flask...
echo URL: http://127.0.0.1:5001
echo.
echo Para detener el servidor: Presiona Ctrl+C
echo ============================================================
echo.

REM Esperar 3 segundos y abrir navegador
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:5001"

REM Iniciar servidor Flask
python run.py

pause
