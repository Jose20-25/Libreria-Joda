# Script para inicializar Git y preparar para GitHub
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Preparando Repositorio Git" -ForegroundColor Cyan
Write-Host "  Libreria JODA" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Git está instalado
try {
    $gitVersion = git --version
    Write-Host "Git detectado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Git no está instalado" -ForegroundColor Red
    Write-Host "Descarga Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    Start-Process "https://git-scm.com/download/win"
    exit 1
}

Write-Host ""
Write-Host "[1/5] Inicializando repositorio Git..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "Repositorio Git ya existe" -ForegroundColor Green
} else {
    git init
    Write-Host "Repositorio Git inicializado" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/5] Configurando archivos..." -ForegroundColor Yellow

# Asegurar que instance/ esté en .gitignore
$gitignoreContent = Get-Content ".gitignore" -Raw
if ($gitignoreContent -notmatch "instance/") {
    Add-Content ".gitignore" "`ninstance/"
}

Write-Host "Archivos configurados" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Agregando archivos al staging..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[4/5] Creando commit inicial..." -ForegroundColor Yellow
git commit -m "Initial commit - Sistema ERP Libreria JODA con Firebase + Render"

Write-Host ""
Write-Host "[5/5] Configurando rama principal..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Repositorio Git Listo" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Crea un repositorio en GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Conecta tu repositorio local:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/TU_USUARIO/libreria-joda.git" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Sube tu codigo:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Ve a Render.com y conecta tu repositorio:" -ForegroundColor White
Write-Host "   https://dashboard.render.com/create?type=web" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Enter para abrir GitHub..." -ForegroundColor Yellow
Read-Host

Start-Process "https://github.com/new"
