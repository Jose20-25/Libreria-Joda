# 🔥 Firebase Hosting + Cloud Run - Librería JODA

## 🎯 Configuración Actual

Tu proyecto Firebase está configurado con:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyAfW7SxYRSWnrO-fYY-z8nQu9qyLDXRxPk",
  authDomain: "libreria-joda.firebaseapp.com",
  databaseURL: "https://libreria-joda-default-rtdb.firebaseio.com",
  projectId: "libreria-joda",
  storageBucket: "libreria-joda.firebasestorage.app",
  messagingSenderId: "830839974398",
  appId: "1:830839974398:web:e26fe381b73e60a2f1b8af"
};
```

## 📐 Arquitectura del Despliegue

```
┌─────────────────────────────────────────────────────────┐
│                    FIREBASE HOSTING                      │
│              https://libreria-joda.web.app              │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Archivos Estáticos (CSS, JS, Imágenes)          │ │
│  └────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │ Proxy/Rewrite
                     ▼
┌─────────────────────────────────────────────────────────┐
│                     CLOUD RUN                            │
│            (Backend Python Flask)                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Docker Container                                  │ │
│  │  - Flask App                                       │ │
│  │  - Gunicorn Server                                 │ │
│  │  - Python 3.11                                     │ │
│  └────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                           │
│                                                          │
│  Opción 1: SQLite (en contenedor - no persistente)     │
│  Opción 2: Cloud SQL PostgreSQL (recomendado)          │
│  Opción 3: Firestore (NoSQL de Firebase)               │
└─────────────────────────────────────────────────────────┘
```

## ⚠️ IMPORTANTE: Persistencia de Datos

### Problema con SQLite en Cloud Run

Cloud Run es **stateless** (sin estado), lo que significa:
- ❌ Los datos en SQLite se pierden cuando el contenedor se reinicia
- ❌ No hay persistencia entre despliegues
- ❌ No es adecuado para producción

### ✅ Soluciones Recomendadas

#### 1. Cloud SQL (PostgreSQL) - **RECOMENDADO**

**Ventajas:**
- ✅ Base de datos completamente gestionada
- ✅ Backups automáticos
- ✅ Alta disponibilidad
- ✅ Compatible con SQLAlchemy (sin cambios en código)

**Configuración:**
```powershell
# Ver INICIO_RAPIDO_DESPLIEGUE.md sección "Base de Datos Persistente"
```

**Costo:** ~$7-10 USD/mes (tier más pequeño)

#### 2. Firestore - **ALTERNATIVA**

**Ventajas:**
- ✅ Base de datos NoSQL de Firebase
- ✅ Integración nativa con Firebase
- ✅ Sincronización en tiempo real
- ✅ Generoso plan gratuito

**Desventajas:**
- ⚠️ Requiere reescribir modelos (no usa SQLAlchemy)
- ⚠️ Modelo de datos diferente (NoSQL vs SQL)

**Costo:** Gratis hasta cierto límite, luego ~$1-5 USD/mes

#### 3. SQLite + Cloud Storage - **NO RECOMENDADO**

Solo para desarrollo/pruebas, no para producción.

## 🚀 Proceso de Despliegue

### 1. Pre-Verificación
```powershell
.\verificar_despliegue.ps1
```

### 2. Backup de Datos
```powershell
python exportar_datos.py
```

### 3. Despliegue
```powershell
.\deploy.ps1
```

### 4. Restaurar Datos
```powershell
python importar_datos.py datos_backup_YYYYMMDD_HHMMSS.json
```

## 📊 Costos Estimados

### Configuración Básica (SQLite temporal)
- Firebase Hosting: **GRATIS** (hasta 10GB/mes)
- Cloud Run: **GRATIS** (primeros 2M requests/mes)
- **Total: $0 USD/mes** ⚠️ Pero SIN persistencia

### Configuración Producción (Cloud SQL)
- Firebase Hosting: **GRATIS**
- Cloud Run: **GRATIS** (bajo tráfico)
- Cloud SQL (db-f1-micro): **~$7-10 USD/mes**
- **Total: ~$7-10 USD/mes** ✅ Con persistencia completa

### Configuración Firestore
- Firebase Hosting: **GRATIS**
- Cloud Run: **GRATIS**
- Firestore: **GRATIS** (hasta 50K lecturas/día)
- **Total: ~$0-5 USD/mes** ✅ Con persistencia

## 🔒 Seguridad

### Variables de Entorno a Configurar

```powershell
# Generar clave secreta segura
python -c "import secrets; print(secrets.token_hex(32))"

# Configurar en Cloud Run
gcloud run services update libreria-joda `
    --region=us-central1 `
    --set-env-vars="SECRET_KEY=tu-clave-generada-aqui"
```

### Firewall y Acceso

Por defecto, Cloud Run es público. Para restringir:

```powershell
# Solo usuarios autenticados
gcloud run services update libreria-joda `
    --region=us-central1 `
    --no-allow-unauthenticated
```

## 📈 Escalabilidad

Cloud Run escala automáticamente:
- **Mínimo:** 0 instancias (no paga cuando no hay tráfico)
- **Máximo:** 100 instancias (configurable)
- **Tiempo de arranque:** ~2-3 segundos

```powershell
# Configurar límites
gcloud run services update libreria-joda `
    --region=us-central1 `
    --min-instances=0 `
    --max-instances=10
```

## 🔍 Monitoreo

### Logs en Tiempo Real
```powershell
gcloud run services logs tail libreria-joda --region=us-central1
```

### Dashboard
- Cloud Run: https://console.cloud.google.com/run
- Firebase: https://console.firebase.google.com

### Métricas
- Requests por segundo
- Latencia
- Uso de memoria
- Errores 4xx/5xx

## 🆘 Troubleshooting

### "Cold Start" lento
**Síntoma:** Primera petición tarda 3-5 segundos

**Solución:**
```powershell
# Mantener 1 instancia siempre activa (cuesta dinero)
gcloud run services update libreria-joda `
    --region=us-central1 `
    --min-instances=1
```

### Datos se pierden
**Síntoma:** Después de reiniciar, los datos no están

**Solución:** Configurar Cloud SQL (ver INICIO_RAPIDO_DESPLIEGUE.md)

### Error 502/503
**Síntoma:** Aplicación no responde

**Diagnóstico:**
```powershell
gcloud run services logs read libreria-joda --region=us-central1 --limit=50
```

## 📚 Recursos

- [Documentación Firebase Hosting](https://firebase.google.com/docs/hosting)
- [Documentación Cloud Run](https://cloud.google.com/run/docs)
- [Guía Completa de Despliegue](GUIA_DESPLIEGUE_FIREBASE.md)
- [Inicio Rápido](INICIO_RAPIDO_DESPLIEGUE.md)

## 🎓 Próximos Pasos

1. ✅ Verificar requisitos: `.\verificar_despliegue.ps1`
2. ✅ Exportar datos: `python exportar_datos.py`
3. ✅ Desplegar: `.\deploy.ps1`
4. ⚙️ Configurar Cloud SQL para persistencia
5. 🔒 Configurar variables de entorno seguras
6. 📊 Configurar monitoreo y alertas
7. 🔄 Configurar CI/CD con GitHub Actions
