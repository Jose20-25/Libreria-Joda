# Despliegue Completo - Firebase Hosting + Render
# Stack: Firebase (Frontend) + Render (Backend) + PostgreSQL

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Despliegue Completo" -ForegroundColor Cyan
Write-Host "  Firebase + GitHub + Render" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuracion:" -ForegroundColor Yellow
Write-Host "- Frontend: Firebase Hosting (GRATIS)" -ForegroundColor Green
Write-Host "- Codigo: GitHub (respaldo)" -ForegroundColor Green
Write-Host "- Backend: Render.com (GRATIS)" -ForegroundColor Green
Write-Host "- Base datos: PostgreSQL Render (GRATIS)" -ForegroundColor Green
Write-Host ""

# Verificar Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Git no encontrado. Reinicia PowerShell despues de la instalacion" -ForegroundColor Red
    exit 1
}

# Backup
Write-Host ""
Write-Host "[1/6] Verificando backup..." -ForegroundColor Yellow
$backup = Get-ChildItem -Path "datos_backup_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Write-Host "Backup: $($backup.Name)" -ForegroundColor Green
} else {
    Write-Host "Creando backup..." -ForegroundColor Yellow
    python exportar_datos.py
}

# Configurar Git
Write-Host ""
Write-Host "[2/6] Configurando Git..." -ForegroundColor Yellow
$userName = git config --global user.name 2>$null
if (-not $userName) {
    git config --global user.name "jose20-25"
    git config --global user.email "jose20-25@users.noreply.github.com"
    Write-Host "Git configurado" -ForegroundColor Green
} else {
    Write-Host "Git ya configurado: $userName" -ForegroundColor Green
}

# Inicializar repo
Write-Host ""
Write-Host "[3/6] Preparando repositorio..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

git remote remove origin 2>$null
git remote add origin https://github.com/jose20-25/Libreria-Joda.git
Write-Host "Repositorio configurado" -ForegroundColor Green

# Preparar archivos para Firebase Hosting
Write-Host ""
Write-Host "[4/6] Preparando archivos para Firebase..." -ForegroundColor Yellow

# Copiar archivos estáticos a public para Firebase
if (-not (Test-Path "public")) {
    New-Item -ItemType Directory -Path "public" | Out-Null
}

Copy-Item -Path "app/static/*" -Destination "public/" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path "index.html" -Destination "public/index.html" -Force -ErrorAction SilentlyContinue

Write-Host "Archivos preparados para Firebase" -ForegroundColor Green

# Commit
Write-Host ""
Write-Host "[5/6] Creando commit..." -ForegroundColor Yellow
git add .
git commit -m "Deploy: Sistema ERP - GitHub Pages + Render" 2>$null
Write-Host "Commit listo" -ForegroundColor Green

# Push
Write-Host ""
Write-Host "[6/6] Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Cyan
Write-Host "- Usuario: jose20-25" -ForegroundColor White
Write-Host "- Password: TU TOKEN DE GITHUB (no tu contraseña)" -ForegroundColor White
Write-Host ""
Write-Host "Como crear token:" -ForegroundColor Yellow
Write-Host "1. https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "2. Generate new token (classic)" -ForegroundColor Gray
Write-Host "3. Permisos: repo, workflow" -ForegroundColor Gray
Write-Host "4. Copia el token generado" -ForegroundColor Gray
Write-Host ""

$continuar = Read-Host "Hacer push ahora? (s/n)"
if ($continuar -eq "s" -or $continuar -eq "S" -or $continuar -eq "") {
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "======================================" -ForegroundColor Green
        Write-Host "  EXITO - Codigo en GitHub" -ForegroundColor Green
        Write-Host "======================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora desplegando en Firebase..." -ForegroundColor Yellow
        
        # Desplegar en Firebase
        firebase deploy --only hosting
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "Firebase Hosting desplegado en:" -ForegroundColor Green
            Write-Host "https://libreria-joda.web.app" -ForegroundColor Cyan
            Write-Host ""
        }
        
        Write-Host "Siguiente: Configurar backend en Render:" -ForegroundColor Yellow
        Write-Host "1. Ve a: https://dashboard.render.com/register" -ForegroundColor White
        Write-Host "2. Conecta con GitHub" -ForegroundColor White
        Write-Host "3. Selecciona: Libreria-Joda" -ForegroundColor White
        Write-Host "4. Configura como Web Service:" -ForegroundColor White
        Write-Host "   - Name: libreria-joda" -ForegroundColor Gray
        Write-Host "   - Environment: Python 3"y Firebase ahora? (s/n)"
        if ($abrirRender -eq "s" -or $abrirRender -eq "S" -or $abrirRender -eq "") {
            Start-Process "https://libreria-joda.web.app"
            Start-Process "https://dashboard.render.com/register"
            Start-Process "https://github.com/jose20-25/Libreria-Joda
        Write-Host "5. Variables de entorno:" -ForegroundColor White
        Write-Host "   FLASK_ENV = production" -ForegroundColor Gray
        Write-Host "   SECRET_KEY = (genera uno aleatorio)" -ForegroundColor Gray
        Write-Host ""
        
        $abrirRender = Read-Host "Abrir Render ahora? (s/n)"
        if ($abrirRender -eq "s" -or $abrirRender -eq "S" -or $abrirRender -eq "") {
            Start-Process "https://dashboard.render.com/register"
            Start-Process "https://jose20-25.github.io/Libreria-Joda/"
            Start-Process "INSTRUCCIONES_DESPLIEGUE_GRATIS.html"
        }
    } else {
        Write-Host ""
        Write-Host "Error al hacer push. Verifica:" -ForegroundColor Red
        Write-Host "1. Token valido" -ForegroundColor Yellow
        Write-Host "2. Permisos correctos (repo, workflow)" -ForegroundColor Yellow
        Write-Host "3. Repositorio existe: https://github.com/jose20-25/Libreria-Joda" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Puedes hacer push manualmente con:" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Credenciales del sistema:" -ForegroundColor Yellow
Write-Host "Usuario: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""
