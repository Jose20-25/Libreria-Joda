# Script de verificacion pre-despliegue

Write-Host ""
Write-Host "VERIFICACION PRE-DESPLIEGUE - Libreria JODA" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gray
Write-Host ""

$errores = 0
$advertencias = 0

# Verificar Firebase CLI
Write-Host "Verificando Firebase CLI..." -NoNewline
try {
    $null = firebase --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " NO INSTALADO" -ForegroundColor Red
        Write-Host "   Instalar con: npm install -g firebase-tools" -ForegroundColor Yellow
        $errores++
    }
} catch {
    Write-Host " NO INSTALADO" -ForegroundColor Red
    Write-Host "   Instalar con: npm install -g firebase-tools" -ForegroundColor Yellow
    $errores++
}

# Verificar Google Cloud SDK
Write-Host "Verificando Google Cloud SDK..." -NoNewline
try {
    $null = gcloud version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " NO INSTALADO" -ForegroundColor Red
        Write-Host "   Descargar desde: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
        $errores++
    }
} catch {
    Write-Host " NO INSTALADO" -ForegroundColor Red
    Write-Host "   Descargar desde: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    $errores++
}

# Verificar archivos necesarios
Write-Host ""
Write-Host "Verificando archivos de configuracion..." -ForegroundColor Cyan

$archivosRequeridos = @(
    "firebase.json",
    ".firebaserc",
    "Dockerfile",
    "cloudbuild.yaml",
    "requirements.txt",
    "run.py"
)

foreach ($archivo in $archivosRequeridos) {
    Write-Host "   $archivo..." -NoNewline
    if (Test-Path $archivo) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " NO ENCONTRADO" -ForegroundColor Red
        $errores++
    }
}

# Verificar backup de datos
Write-Host ""
Write-Host "Verificando backup de datos..." -ForegroundColor Cyan
$backupFiles = Get-ChildItem -Filter "datos_backup_*.json" -ErrorAction SilentlyContinue

if ($backupFiles.Count -gt 0) {
    Write-Host "   OK - Backup encontrado: $($backupFiles[0].Name)" -ForegroundColor Green
    Write-Host "   Fecha: $($backupFiles[0].LastWriteTime)" -ForegroundColor Gray
} else {
    Write-Host "   ADVERTENCIA - No se encontro backup reciente" -ForegroundColor Yellow
    Write-Host "   RECOMENDADO: Ejecutar python exportar_datos.py antes de desplegar" -ForegroundColor Yellow
    $advertencias++
}

# Verificar base de datos actual
Write-Host ""
Write-Host "Verificando base de datos..." -ForegroundColor Cyan
if (Test-Path "instance/libreria_joda.db") {
    $dbSize = [math]::Round((Get-Item "instance/libreria_joda.db").Length / 1KB, 2)
    Write-Host "   OK - Base de datos encontrada ($dbSize KB)" -ForegroundColor Green
} elseif (Test-Path "libreria_joda.db") {
    $dbSize = [math]::Round((Get-Item "libreria_joda.db").Length / 1KB, 2)
    Write-Host "   OK - Base de datos encontrada ($dbSize KB)" -ForegroundColor Green
} else {
    Write-Host "   ADVERTENCIA - No se encontro base de datos local" -ForegroundColor Yellow
    $advertencias++
}

# Resumen
Write-Host ""
Write-Host "============================================================" -ForegroundColor Gray
Write-Host ""

if ($errores -eq 0 -and $advertencias -eq 0) {
    Write-Host "TODO LISTO PARA DESPLEGAR" -ForegroundColor Green
    Write-Host ""
    Write-Host "Siguiente paso:" -ForegroundColor Cyan
    Write-Host "   .\deploy.ps1" -ForegroundColor White
} elseif ($errores -eq 0) {
    Write-Host "LISTO CON ADVERTENCIAS ($advertencias)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Puedes continuar con el despliegue, pero revisa las advertencias." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Siguiente paso:" -ForegroundColor Cyan
    Write-Host "   .\deploy.ps1" -ForegroundColor White
} else {
    Write-Host "NO LISTO PARA DESPLEGAR" -ForegroundColor Red
    Write-Host ""
    Write-Host "Errores encontrados: $errores" -ForegroundColor Red
    Write-Host "Advertencias: $advertencias" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Por favor corrige los errores antes de continuar." -ForegroundColor Yellow
}

Write-Host ""
