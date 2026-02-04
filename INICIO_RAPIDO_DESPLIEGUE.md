# 🚀 PASOS RÁPIDOS PARA DESPLEGAR EN FIREBASE

## ⚠️ PASO 1: EXPORTAR DATOS ACTUALES (NO PERDER INFORMACIÓN)

**IMPORTANTE**: Antes de hacer cualquier cosa, guarda tus datos:

```powershell
python exportar_datos.py
```

Esto creará un archivo `datos_backup_YYYYMMDD_HHMMSS.json` con toda tu información.

---

## 📦 PASO 2: INSTALAR HERRAMIENTAS

### Instalar Firebase CLI:
```powershell
npm install -g firebase-tools
```

### Instalar Google Cloud SDK:
Descarga desde: https://cloud.google.com/sdk/docs/install

---

## 🔐 PASO 3: AUTENTICACIÓN

```powershell
# Firebase
firebase login

# Google Cloud
gcloud auth login
gcloud config set project libreria-joda
```

---

## 🎯 PASO 4: HABILITAR SERVICIOS DE GOOGLE CLOUD

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

---

## 🚀 PASO 5: DESPLEGAR (AUTOMÁTICO)

### Opción A: Despliegue Automático (Recomendado)
```powershell
.\deploy.ps1
```

### Opción B: Despliegue Manual

1. **Build y Deploy Backend:**
```powershell
gcloud builds submit --config cloudbuild.yaml
```

2. **Deploy Hosting:**
```powershell
firebase deploy --only hosting
```

---

## 📥 PASO 6: RESTAURAR DATOS

Después de desplegar, importa tus datos:

```powershell
# Busca el archivo de backup que creaste en el PASO 1
python importar_datos.py datos_backup_YYYYMMDD_HHMMSS.json
```

---

## ✅ VERIFICAR DESPLIEGUE

Tu aplicación estará disponible en:
- **https://libreria-joda.web.app**
- **https://libreria-joda.firebaseapp.com**

---

## 💾 CONFIGURAR BASE DE DATOS PERSISTENTE (Opcional pero Recomendado)

### Para que los datos NO se pierdan al reiniciar:

#### Opción 1: Cloud SQL (PostgreSQL)

```powershell
# Crear instancia
gcloud sql instances create libreria-joda-db `
    --database-version=POSTGRES_14 `
    --tier=db-f1-micro `
    --region=us-central1

# Crear base de datos
gcloud sql databases create libreria_joda --instance=libreria-joda-db

# Crear usuario
gcloud sql users create libreria-user `
    --instance=libreria-joda-db `
    --password=TU_PASSWORD_SEGURO

# Configurar Cloud Run para usar Cloud SQL
gcloud run services update libreria-joda `
    --region=us-central1 `
    --add-cloudsql-instances=libreria-joda:us-central1:libreria-joda-db `
    --set-env-vars="CLOUD_SQL_CONNECTION_NAME=libreria-joda:us-central1:libreria-joda-db,DB_USER=libreria-user,DB_PASS=TU_PASSWORD_SEGURO,DB_NAME=libreria_joda"
```

#### Opción 2: Firestore (NoSQL de Firebase)

Si prefieres usar Firestore, tendríamos que adaptar los modelos.

---

## 🔒 CONFIGURAR VARIABLES DE ENTORNO SEGURAS

```powershell
gcloud run services update libreria-joda `
    --region=us-central1 `
    --set-env-vars="SECRET_KEY=genera-una-clave-segura-aqui,FLASK_ENV=production"
```

---

## 📊 MONITOREO

### Ver logs en tiempo real:
```powershell
gcloud run services logs tail libreria-joda --region=us-central1
```

### Ver dashboard:
https://console.cloud.google.com/run/detail/us-central1/libreria-joda

---

## ⚠️ SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "Permission denied"
```powershell
gcloud auth login
firebase login --reauth
```

### Error: "Service not found"
Verifica que el proyecto esté configurado:
```powershell
gcloud config get-value project
firebase use libreria-joda
```

### Error: "Build failed"
Verifica que Dockerfile esté correcto y que todas las dependencias estén en requirements.txt

---

## 🆘 AYUDA

- **Documentación completa**: Ver [GUIA_DESPLIEGUE_FIREBASE.md](GUIA_DESPLIEGUE_FIREBASE.md)
- **Firebase Console**: https://console.firebase.google.com
- **Google Cloud Console**: https://console.cloud.google.com
