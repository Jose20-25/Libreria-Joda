# Script de instalación y ejecución para LIBRERÍA JODA ERP
# Ejecutar con: .\install_and_run.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   LIBRERÍA JODA - Sistema ERP con Python" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Python instalado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "   Python no encontrado" -ForegroundColor Red
    Write-Host "   Por favor instala Python desde: https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "   Asegurate de marcar Add Python to PATH durante la instalacion" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "2. Verificando entorno virtual..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "   ✓ Entorno virtual ya existe" -ForegroundColor Green
} else {
    Write-Host "   Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "   ✓ Entorno virtual creado" -ForegroundColor Green
}

Write-Host ""
Write-Host "3. Activando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "4. Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green

Write-Host ""
Write-Host "5. Verificando base de datos..." -ForegroundColor Yellow
if (Test-Path "libreria_joda.db") {
    Write-Host "   ✓ Base de datos ya existe" -ForegroundColor Green
} else {
    Write-Host "   Se creará automáticamente al iniciar..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Instalacion completada!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Accede al sistema en: http://localhost:5001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales de acceso:" -ForegroundColor Yellow
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contrasena: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar el servidor
python run.py
