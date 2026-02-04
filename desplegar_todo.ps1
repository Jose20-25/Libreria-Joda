# Script completo de despliegue con GitHub y Render
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Despliegue Completo - Libreria JODA" -ForegroundColor Cyan
Write-Host "  GitHub + Render + Firebase" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Crear backup
Write-Host "[1/7] Creando backup de datos..." -ForegroundColor Yellow
$backupFiles = Get-ChildItem -Path "datos_backup_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
if ($backupFiles.Count -eq 0) {
    python exportar_datos.py
    Write-Host "Backup creado" -ForegroundColor Green
} else {
    Write-Host "Backup encontrado: $($backupFiles[0].Name)" -ForegroundColor Green
}

# Paso 2: Inicializar Git
Write-Host ""
Write-Host "[2/7] Inicializando Git..." -ForegroundColor Yellow
if (-Not (Test-Path ".git")) {
    git init
    git branch -M main
    Write-Host "Git inicializado" -ForegroundColor Green
} else {
    Write-Host "Git ya inicializado" -ForegroundColor Green
}

# Paso 3: Commit
Write-Host ""
Write-Host "[3/7] Agregando archivos..." -ForegroundColor Yellow
git add .
git commit -m "Deploy: Sistema ERP Libreria JODA" -ErrorAction SilentlyContinue
Write-Host "Commit creado" -ForegroundColor Green

# Paso 4: Instrucciones para GitHub
Write-Host ""
Write-Host "[4/7] Configurar GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Abre GitHub y crea un repositorio llamado: libreria-joda" -ForegroundColor Cyan
Write-Host ""
$openGithub = Read-Host "Presiona Enter para abrir GitHub (o escribe 'skip' para omitir)"

if ($openGithub -ne "skip") {
    Start-Process "https://github.com/new"
    Write-Host ""
    Write-Host "Despues de crear el repositorio, copia la URL y pegala aqui:" -ForegroundColor Yellow
    $repoUrl = Read-Host "URL del repositorio"
    
    if ($repoUrl) {
        git remote remove origin -ErrorAction SilentlyContinue
        git remote add origin $repoUrl
        Write-Host "Subiendo codigo a GitHub..." -ForegroundColor Yellow
        git push -u origin main
        Write-Host "Codigo subido a GitHub" -ForegroundColor Green
    }
}

# Paso 5: Preparar Firebase
Write-Host ""
Write-Host "[5/7] Preparando Firebase..." -ForegroundColor Yellow
if (-Not (Test-Path "public")) {
    New-Item -ItemType Directory -Path "public" | Out-Null
}
Copy-Item -Path "app/static/*" -Destination "public/" -Recurse -Force
Copy-Item -Path "public_index.html" -Destination "public/index.html" -Force
Write-Host "Archivos preparados" -ForegroundColor Green

# Paso 6: Desplegar Firebase
Write-Host ""
Write-Host "[6/7] Desplegando en Firebase..." -ForegroundColor Yellow
firebase deploy --only hosting
Write-Host "Firebase desplegado" -ForegroundColor Green

# Paso 7: Instrucciones Render
Write-Host ""
Write-Host "[7/7] Configurar Render..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Ahora ve a Render.com:" -ForegroundColor Cyan
Write-Host "1. Registrate con GitHub" -ForegroundColor White
Write-Host "2. Click 'New +' -> 'Web Service'" -ForegroundColor White
Write-Host "3. Selecciona tu repositorio 'libreria-joda'" -ForegroundColor White
Write-Host "4. Configuracion:" -ForegroundColor White
Write-Host "   - Name: libreria-joda" -ForegroundColor Gray
Write-Host "   - Environment: Python 3" -ForegroundColor Gray
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   - Start Command: gunicorn -w 1 -b 0.0.0.0:`$PORT run:app" -ForegroundColor Gray
Write-Host "   - Plan: Free" -ForegroundColor Gray
Write-Host "5. Agrega variables de entorno:" -ForegroundColor White
Write-Host "   - FLASK_ENV = production" -ForegroundColor Gray
Write-Host "   - SECRET_KEY = (genera un valor aleatorio)" -ForegroundColor Gray
Write-Host ""
$openRender = Read-Host "Presiona Enter para abrir Render.com"

if ($openRender -ne "skip") {
    Start-Process "https://dashboard.render.com/register"
    Start-Process "INSTRUCCIONES_DESPLIEGUE_GRATIS.html"
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Despliegue Iniciado" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Yellow
Write-Host "Firebase: https://libreria-joda.web.app" -ForegroundColor Cyan
Write-Host "GitHub: (tu repositorio)" -ForegroundColor Cyan
Write-Host "Render: (se generara despues del deploy)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales:" -ForegroundColor Yellow
Write-Host "Usuario: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""
