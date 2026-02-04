# Script de Despliegue 100% Gratuito - Firebase + Render
# Sin necesidad de tarjeta de crédito

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Despliegue Gratuito - Librería JODA" -ForegroundColor Cyan
Write-Host "  Firebase Hosting + Render.com" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el backup de datos
$backupFiles = Get-ChildItem -Path "datos_backup_*.json" | Sort-Object LastWriteTime -Descending
if ($backupFiles.Count -eq 0) {
    Write-Host "[1/5] Creando backup de datos..." -ForegroundColor Yellow
    python exportar_datos.py
} else {
    Write-Host "[1/5] ✓ Backup encontrado: $($backupFiles[0].Name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/5] Preparando archivos para Firebase Hosting..." -ForegroundColor Yellow

# Crear directorio public si no existe
if (-Not (Test-Path "public")) {
    New-Item -ItemType Directory -Path "public" | Out-Null
}

# Copiar archivos estáticos
Copy-Item -Path "app/static/*" -Destination "public/" -Recurse -Force

# Copiar página de bienvenida
Copy-Item -Path "public_index.html" -Destination "public/index.html" -Force

Write-Host "[2/5] ✓ Archivos preparados" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Configurando Firebase Hosting..." -ForegroundColor Yellow

# Actualizar firebase.json para hosting simple
@"
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ]
  }
}
"@ | Out-File -FilePath "firebase.json" -Encoding UTF8

Write-Host "[3/5] ✓ Firebase configurado" -ForegroundColor Green

Write-Host ""
Write-Host "[4/5] Desplegando en Firebase Hosting..." -ForegroundColor Yellow
firebase deploy --only hosting

if ($LASTEXITCODE -eq 0) {
    Write-Host "[4/5] ✓ Firebase Hosting desplegado" -ForegroundColor Green
} else {
    Write-Host "[4/5] ✗ Error en despliegue de Firebase" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[5/5] Abriendo instrucciones..." -ForegroundColor Yellow
Start-Process "INSTRUCCIONES_DESPLIEGUE_GRATIS.html"

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  ✓ Despliegue Completado" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Firebase Hosting: " -NoNewline
Write-Host "https://libreria-joda.web.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Sube tu código a GitHub" -ForegroundColor White
Write-Host "2. Crea cuenta en Render.com (gratis, sin tarjeta)" -ForegroundColor White
Write-Host "3. Despliega el backend en Render" -ForegroundColor White
Write-Host "4. Conecta Firebase con Render" -ForegroundColor White
Write-Host ""
Write-Host "Credenciales:" -ForegroundColor Yellow
Write-Host "Usuario: admin" -ForegroundColor White
Write-Host "Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Ver README_DESPLIEGUE.md para instrucciones completas" -ForegroundColor Cyan
Write-Host ""

