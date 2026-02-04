# Script de configuración completa para GitHub Pages + Render
# Repositorio: https://github.com/jose20-25/Libreria-Joda

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Configuracion Completa" -ForegroundColor Cyan
Write-Host "  Libreria JODA - GitHub + Render" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Verificar/Instalar Git
Write-Host "[1/8] Verificando Git..." -ForegroundColor Yellow

try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Git instalado: $gitVersion" -ForegroundColor Green
    } else {
        throw "Git no encontrado"
    }
} catch {
    Write-Host "Git no esta instalado. Instalando..." -ForegroundColor Yellow
    
    # Descargar Git
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$env:TEMP\GitInstaller.exe"
    
    Write-Host "Descargando Git..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
    
    Write-Host "Instalando Git (esto puede tomar unos minutos)..." -ForegroundColor Yellow
    Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT /NORESTART" -Wait
    
    # Actualizar PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "Git instalado correctamente" -ForegroundColor Green
    Write-Host "IMPORTANTE: Cierra y vuelve a abrir PowerShell, luego ejecuta este script nuevamente" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar"
    exit 0
}

# Paso 2: Crear backup
Write-Host ""
Write-Host "[2/8] Creando backup de datos..." -ForegroundColor Yellow
$backupFiles = Get-ChildItem -Path "datos_backup_*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
if ($backupFiles.Count -eq 0) {
    python exportar_datos.py
    Write-Host "Backup creado" -ForegroundColor Green
} else {
    Write-Host "Backup encontrado: $($backupFiles[0].Name)" -ForegroundColor Green
}

# Paso 3: Configurar Git
Write-Host ""
Write-Host "[3/8] Configurando Git..." -ForegroundColor Yellow

$gitName = git config --global user.name 2>$null
$gitEmail = git config --global user.email 2>$null

if (-not $gitName) {
    Write-Host "Configura tu nombre de usuario de Git:" -ForegroundColor Cyan
    $nombre = Read-Host "Tu nombre"
    git config --global user.name "$nombre"
}

if (-not $gitEmail) {
    Write-Host "Configura tu email de Git:" -ForegroundColor Cyan
    $email = Read-Host "Tu email"
    git config --global user.email "$email"
}

Write-Host "Git configurado correctamente" -ForegroundColor Green

# Paso 4: Inicializar repositorio
Write-Host ""
Write-Host "[4/8] Inicializando repositorio..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
    Write-Host "Repositorio inicializado" -ForegroundColor Green
} else {
    Write-Host "Repositorio ya existe" -ForegroundColor Green
}

# Paso 5: Configurar remoto
Write-Host ""
Write-Host "[5/8] Configurando repositorio remoto..." -ForegroundColor Yellow

$remoteUrl = "https://github.com/jose20-25/Libreria-Joda.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "Remoto configurado: $remoteUrl" -ForegroundColor Green

# Paso 6: Commit
Write-Host ""
Write-Host "[6/8] Creando commit..." -ForegroundColor Yellow
git add .
git commit -m "Deploy: Sistema ERP completo con Firebase + Render" -ErrorAction SilentlyContinue
Write-Host "Commit creado" -ForegroundColor Green

# Paso 7: Push a GitHub
Write-Host ""
Write-Host "[7/8] Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Sube el codigo a GitHub con:" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Si es la primera vez, te pedira autenticacion:" -ForegroundColor Yellow
Write-Host "- Usuario: jose20-25" -ForegroundColor Gray
Write-Host "- Password: (tu token de acceso personal de GitHub)" -ForegroundColor Gray
Write-Host ""
Write-Host "Como crear un token:" -ForegroundColor Yellow
Write-Host "1. Ve a GitHub -> Settings -> Developer settings -> Personal access tokens" -ForegroundColor Gray
Write-Host "2. Generate new token (classic)" -ForegroundColor Gray
Write-Host "3. Marca: repo, workflow" -ForegroundColor Gray
Write-Host "4. Genera y copia el token" -ForegroundColor Gray
Write-Host ""

$continuar = Read-Host "Quieres hacer push ahora? (s/n)"
if ($continuar -eq "s" -or $continuar -eq "S") {
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Codigo subido exitosamente" -ForegroundColor Green
    } else {
        Write-Host "Error al subir. Verifica tus credenciales" -ForegroundColor Red
    }
}

# Paso 8: Preparar despliegues
Write-Host ""
Write-Host "[8/8] Preparando despliegues..." -ForegroundColor Yellow

# Firebase
if (-not (Test-Path "public")) {
    New-Item -ItemType Directory -Path "public" | Out-Null
}
Copy-Item -Path "app/static/*" -Destination "public/" -Recurse -Force
Copy-Item -Path "public_index.html" -Destination "public/index.html" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Configuracion Completada" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "URLs de tu proyecto:" -ForegroundColor Yellow
Write-Host "GitHub: https://github.com/jose20-25/Libreria-Joda" -ForegroundColor Cyan
Write-Host "GitHub Pages: https://jose20-25.github.io/Libreria-Joda/" -ForegroundColor Cyan
Write-Host "Firebase: https://libreria-joda.web.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. GitHub Pages esta listo en: https://jose20-25.github.io/Libreria-Joda/" -ForegroundColor White
Write-Host "2. Despliega en Firebase: firebase deploy --only hosting" -ForegroundColor White
Write-Host "3. Despliega backend en Render:" -ForegroundColor White
Write-Host "   - Ve a https://dashboard.render.com/register" -ForegroundColor Gray
Write-Host "   - Conecta con GitHub" -ForegroundColor Gray
Write-Host "   - Selecciona el repositorio: Libreria-Joda" -ForegroundColor Gray
Write-Host "   - Configura como Web Service (Python)" -ForegroundColor Gray
Write-Host ""
Write-Host "Credenciales del sistema:" -ForegroundColor Yellow
Write-Host "Usuario: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Abriendo recursos..." -ForegroundColor Yellow
Start-Process "https://jose20-25.github.io/Libreria-Joda/"
Start-Process "https://dashboard.render.com/register"
Start-Process "INSTRUCCIONES_DESPLIEGUE_GRATIS.html"
