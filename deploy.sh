#!/bin/bash

# Script para desplegar en Firebase/Cloud Run

echo "🚀 Iniciando despliegue de Librería JODA..."

# Verificar que Firebase CLI está instalado
if ! command -v firebase &> /dev/null
then
    echo "❌ Firebase CLI no está instalado. Instalando..."
    npm install -g firebase-tools
fi

# Verificar que Google Cloud SDK está instalado
if ! command -v gcloud &> /dev/null
then
    echo "❌ Google Cloud SDK no está instalado. Por favor instálalo desde:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Login a Firebase (si es necesario)
echo "📝 Verificando autenticación Firebase..."
firebase login

# Configurar proyecto
echo "⚙️  Configurando proyecto..."
firebase use libreria-joda

# Build y Deploy a Cloud Run
echo "🏗️  Construyendo y desplegando backend..."
gcloud builds submit --config cloudbuild.yaml

# Obtener URL de Cloud Run
CLOUD_RUN_URL=$(gcloud run services describe libreria-joda --region=us-central1 --format='value(status.url)')
echo "✅ Backend desplegado en: $CLOUD_RUN_URL"

# Deploy a Firebase Hosting
echo "🌐 Desplegando hosting..."
firebase deploy --only hosting

echo "✅ ¡Despliegue completado exitosamente!"
echo "🌍 Tu aplicación está disponible en: https://libreria-joda.web.app"
