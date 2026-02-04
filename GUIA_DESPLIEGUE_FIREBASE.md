# 🚀 Guía de Despliegue en Firebase/Cloud Run

## 📋 Prerequisitos

### 1. Instalar Firebase CLI
```bash
npm install -g firebase-tools
```

### 2. Instalar Google Cloud SDK
Descarga e instala desde: https://cloud.google.com/sdk/docs/install

### 3. Configurar proyecto Firebase
Tu proyecto ya está configurado con:
- **Project ID**: libreria-joda
- **Database URL**: https://libreria-joda-default-rtdb.firebaseio.com
- **Region**: us-central1

## 🔐 Autenticación

### Iniciar sesión en Firebase
```bash
firebase login
```

### Iniciar sesión en Google Cloud
```bash
gcloud auth login
gcloud config set project libreria-joda
```

## 📦 Preparar los Datos (IMPORTANTE - Para No Perder Datos)

### Opción 1: Exportar datos de SQLite actual

Ejecuta este script para exportar tus datos actuales:

```bash
python exportar_datos.py
```

Esto creará un archivo `datos_backup.json` con todos tus datos.

### Opción 2: Migrar a Cloud SQL (Recomendado para producción)

Para no perder datos y tener una base de datos persistente:

1. Crear base de datos PostgreSQL en Cloud SQL:
```bash
gcloud sql instances create libreria-joda-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1
```

2. Crear base de datos:
```bash
gcloud sql databases create libreria_joda --instance=libreria-joda-db
```

3. Actualizar `config/config.py` con la conexión a PostgreSQL.

### Opción 3: Cloud Storage para SQLite (Más simple)

Si quieres mantener SQLite pero con persistencia:

1. Los datos se guardarán en Cloud Storage automáticamente
2. El Dockerfile ya está configurado para crear el directorio `/app/instance`

## 🚀 Despliegue Automático

### En Windows PowerShell:
```powershell
.\deploy.ps1
```

### En Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 🛠️ Despliegue Manual Paso a Paso

### 1. Habilitar APIs necesarias
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Build y Deploy del Backend
```bash
# Construir imagen Docker
gcloud builds submit --tag gcr.io/libreria-joda/libreria-joda

# Desplegar a Cloud Run
gcloud run deploy libreria-joda \
    --image gcr.io/libreria-joda/libreria-joda \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### 3. Deploy a Firebase Hosting
```bash
firebase deploy --only hosting
```

## 🔄 Migrar Datos Existentes

### Después del primer despliegue:

1. Accede a tu aplicación desplegada
2. Crea el usuario administrador:
```bash
# Conectar al contenedor de Cloud Run
gcloud run services proxy libreria-joda --region=us-central1

# En otra terminal
python crear_admin.py
```

3. Importar datos del backup:
```bash
python importar_datos.py datos_backup.json
```

## 🔒 Variables de Entorno (Seguridad)

Para producción, configura variables seguras:

```bash
gcloud run services update libreria-joda \
    --region=us-central1 \
    --set-env-vars="SECRET_KEY=tu-clave-secreta-aqui,FLASK_ENV=production"
```

## 📊 Monitoreo

### Ver logs:
```bash
gcloud run services logs read libreria-joda --region=us-central1
```

### Ver métricas:
Visita: https://console.cloud.google.com/run/detail/us-central1/libreria-joda

## 🌐 URLs de Acceso

- **Hosting**: https://libreria-joda.web.app
- **Hosting (alternativo)**: https://libreria-joda.firebaseapp.com
- **Cloud Run directo**: Se asigna automáticamente

## 💾 Backup Automático

Para configurar backups automáticos:

1. Crea un bucket de Cloud Storage:
```bash
gsutil mb gs://libreria-joda-backups
```

2. Configura un Cloud Function para backups periódicos
3. Los backups se guardarán automáticamente

## ⚠️ IMPORTANTE - Persistencia de Datos

**SQLite en Cloud Run tiene limitaciones**:
- Los datos se pierden cuando el contenedor se reinicia
- Para datos persistentes, usa una de estas opciones:
  - **Cloud SQL** (PostgreSQL/MySQL) - Recomendado
  - **Firestore** - NoSQL de Firebase
  - **Cloud Storage** para archivos SQLite

## 🆘 Solución de Problemas

### Error de autenticación:
```bash
firebase login --reauth
gcloud auth login
```

### Error de permisos:
```bash
gcloud projects add-iam-policy-binding libreria-joda \
    --member="user:tu-email@gmail.com" \
    --role="roles/owner"
```

### Logs de errores:
```bash
firebase hosting:channel:open live
gcloud run services logs tail libreria-joda --region=us-central1
```

## 📞 Soporte

Para más ayuda:
- Firebase: https://firebase.google.com/support
- Cloud Run: https://cloud.google.com/run/docs
