# Script de Despliegue 100% Gratuito - Firebase + Render
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Despliegue Gratuito - Libreria JODA" -ForegroundColor Cyan
Write-Host "  Firebase Hosting + Render.com" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Backup de datos
$backupFiles = Get-ChildItem -Path "datos_backup_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
if ($backupFiles.Count -eq 0) {
    Write-Host "[1/5] Creando backup de datos..." -ForegroundColor Yellow
    python exportar_datos.py
} else {
    Write-Host "[1/5] Backup encontrado: $($backupFiles[0].Name)" -ForegroundColor Green
}

# Paso 2: Preparar archivos
Write-Host ""
Write-Host "[2/5] Preparando archivos para Firebase..." -ForegroundColor Yellow

if (-Not (Test-Path "public")) {
    New-Item -ItemType Directory -Path "public" | Out-Null
}

Copy-Item -Path "app/static/*" -Destination "public/" -Recurse -Force
Copy-Item -Path "public_index.html" -Destination "public/index.html" -Force

Write-Host "[2/5] Archivos preparados" -ForegroundColor Green

# Paso 3: Configurar Firebase
Write-Host ""
Write-Host "[3/5] Configurando Firebase Hosting..." -ForegroundColor Yellow

$firebaseJson = @{
    hosting = @{
        public = "public"
        ignore = @(
            "firebase.json"
            "**/.*"
            "**/node_modules/**"
        )
    }
} | ConvertTo-Json -Depth 10

$firebaseJson | Out-File -FilePath "firebase.json" -Encoding UTF8
Write-Host "[3/5] Firebase configurado" -ForegroundColor Green

# Paso 4: Desplegar
Write-Host ""
Write-Host "[4/5] Desplegando en Firebase Hosting..." -ForegroundColor Yellow
firebase deploy --only hosting

if ($LASTEXITCODE -eq 0) {
    Write-Host "[4/5] Firebase Hosting desplegado correctamente" -ForegroundColor Green
} else {
    Write-Host "[4/5] Error en despliegue" -ForegroundColor Red
    exit 1
}

# Paso 5: Abrir instrucciones
Write-Host ""
Write-Host "[5/5] Abriendo instrucciones..." -ForegroundColor Yellow
Start-Process "INSTRUCCIONES_DESPLIEGUE_GRATIS.html"

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Despliegue Completado" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Firebase Hosting desplegado en:" -ForegroundColor Yellow
Write-Host "https://libreria-joda.web.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. Sube tu codigo a GitHub" -ForegroundColor White
Write-Host "2. Crea cuenta en Render.com" -ForegroundColor White
Write-Host "3. Despliega el backend en Render" -ForegroundColor White
Write-Host "4. Conecta Firebase con Render" -ForegroundColor White
Write-Host ""
Write-Host "Credenciales del sistema:" -ForegroundColor Yellow
Write-Host "Usuario: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Ver README_DESPLIEGUE.md para mas detalles" -ForegroundColor Cyan
Write-Host ""
