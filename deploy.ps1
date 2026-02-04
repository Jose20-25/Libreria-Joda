# Script para desplegar en Firebase/Cloud Run (Windows PowerShell)

Write-Host "🚀 Iniciando despliegue de Librería JODA..." -ForegroundColor Green

# Verificar que Firebase CLI está instalado
try {
    firebase --version | Out-Null
} catch {
    Write-Host "❌ Firebase CLI no está instalado. Instalando..." -ForegroundColor Red
    npm install -g firebase-tools
}

# Verificar que Google Cloud SDK está instalado
try {
    gcloud version | Out-Null
} catch {
    Write-Host "❌ Google Cloud SDK no está instalado. Por favor instálalo desde:" -ForegroundColor Red
    Write-Host "https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Login a Firebase
Write-Host "📝 Verificando autenticación Firebase..." -ForegroundColor Cyan
firebase login

# Configurar proyecto
Write-Host "⚙️  Configurando proyecto..." -ForegroundColor Cyan
firebase use libreria-joda

# Build y Deploy a Cloud Run
Write-Host "🏗️  Construyendo y desplegando backend..." -ForegroundColor Cyan
gcloud builds submit --config cloudbuild.yaml

# Obtener URL de Cloud Run
$CLOUD_RUN_URL = gcloud run services describe libreria-joda --region=us-central1 --format="value(status.url)"
Write-Host "✅ Backend desplegado en: $CLOUD_RUN_URL" -ForegroundColor Green

# Deploy a Firebase Hosting
Write-Host "🌐 Desplegando hosting..." -ForegroundColor Cyan
firebase deploy --only hosting

Write-Host "✅ ¡Despliegue completado exitosamente!" -ForegroundColor Green
Write-Host "🌍 Tu aplicación está disponible en: https://libreria-joda.web.app" -ForegroundColor Yellow
