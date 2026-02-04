# ✅ CHECKLIST DE DESPLIEGUE FIREBASE

## 📋 ANTES DE DESPLEGAR

### 1. Backup de Datos
- [ ] Ejecutar `python exportar_datos.py`
- [ ] Verificar que se creó el archivo `datos_backup_*.json`
- [ ] Guardar copia del archivo en lugar seguro (USB, nube, etc.)

### 2. Requisitos Instalados
- [ ] Node.js y npm instalados
- [ ] Firebase CLI instalado (`npm install -g firebase-tools`)
- [ ] Google Cloud SDK instalado
- [ ] Python 3.11+ instalado

### 3. Autenticación
- [ ] `firebase login` ejecutado exitosamente
- [ ] `gcloud auth login` ejecutado exitosamente
- [ ] Proyecto configurado: `gcloud config set project libreria-joda`

### 4. Archivos de Configuración
- [ ] `firebase.json` presente
- [ ] `.firebaserc` presente
- [ ] `Dockerfile` presente
- [ ] `cloudbuild.yaml` presente
- [ ] `requirements.txt` con gunicorn

## 🚀 DURANTE EL DESPLIEGUE

### 1. Habilitar APIs
- [ ] Cloud Build API habilitada
- [ ] Cloud Run API habilitada
- [ ] Container Registry API habilitada

```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Ejecutar Despliegue
- [ ] Ejecutar `.\verificar_despliegue.ps1` (sin errores)
- [ ] Ejecutar `.\deploy.ps1` o despliegue manual
- [ ] Esperar confirmación de despliegue exitoso

### 3. Verificar Despliegue
- [ ] Acceder a https://libreria-joda.web.app
- [ ] Verificar que la página principal carga
- [ ] Intentar iniciar sesión
- [ ] Verificar logs en Cloud Console

## 📥 DESPUÉS DEL DESPLIEGUE

### 1. Restaurar Datos
- [ ] Ejecutar `python importar_datos.py datos_backup_*.json`
- [ ] Verificar que los datos se importaron correctamente
- [ ] Comprobar productos, clientes, ventas, etc.

### 2. Configuración de Seguridad
- [ ] Generar SECRET_KEY segura
- [ ] Configurar variable de entorno SECRET_KEY en Cloud Run
- [ ] Cambiar contraseñas de administrador (si es necesario)

### 3. Base de Datos Persistente (CRÍTICO)
- [ ] Decidir estrategia de persistencia:
  - [ ] Opción A: Cloud SQL PostgreSQL
  - [ ] Opción B: Firestore
  - [ ] Opción C: Mantener SQLite (solo desarrollo)

### 4. Configuración Producción
- [ ] Variables de entorno configuradas
- [ ] Límites de instancias configurados
- [ ] Dominio personalizado (opcional)
- [ ] SSL/HTTPS verificado

## 🔒 SEGURIDAD

### Variables de Entorno Críticas
```powershell
# Generar clave secreta
python -c "import secrets; print(secrets.token_hex(32))"

# Configurar en Cloud Run
gcloud run services update libreria-joda `
    --region=us-central1 `
    --set-env-vars="SECRET_KEY=CLAVE_GENERADA,FLASK_ENV=production"
```

### Checklist de Seguridad
- [ ] SECRET_KEY cambiada (no usar la de desarrollo)
- [ ] FLASK_ENV=production
- [ ] SESSION_COOKIE_SECURE=True
- [ ] Contraseñas de admin actualizadas
- [ ] Firewall configurado (si es necesario)

## 💾 PERSISTENCIA DE DATOS

### ⚠️ IMPORTANTE - SQLite en Cloud Run NO es persistente

Si usas SQLite (configuración por defecto):
- ❌ Los datos se pierden al reiniciar el contenedor
- ❌ No apto para producción
- ✅ Solo para pruebas/desarrollo

### Solución: Cloud SQL

```powershell
# 1. Crear instancia Cloud SQL
gcloud sql instances create libreria-joda-db `
    --database-version=POSTGRES_14 `
    --tier=db-f1-micro `
    --region=us-central1

# 2. Crear base de datos
gcloud sql databases create libreria_joda --instance=libreria-joda-db

# 3. Crear usuario
gcloud sql users create libreria_user `
    --instance=libreria-joda-db `
    --password=PASSWORD_SEGURO_AQUI

# 4. Conectar Cloud Run a Cloud SQL
gcloud run services update libreria-joda `
    --region=us-central1 `
    --add-cloudsql-instances=libreria-joda:us-central1:libreria-joda-db `
    --set-env-vars="CLOUD_SQL_CONNECTION_NAME=libreria-joda:us-central1:libreria-joda-db,DB_USER=libreria_user,DB_PASS=PASSWORD_SEGURO_AQUI,DB_NAME=libreria_joda"

# 5. Instalar dependencias PostgreSQL (ya incluido en requirements.txt)

# 6. Importar datos
python importar_datos.py datos_backup_*.json
```

Checklist Cloud SQL:
- [ ] Instancia creada
- [ ] Base de datos creada
- [ ] Usuario creado con contraseña segura
- [ ] Cloud Run conectado a Cloud SQL
- [ ] Variables de entorno configuradas
- [ ] Datos importados
- [ ] Backup automático configurado

## 📊 MONITOREO

### Logs y Métricas
- [ ] Revisar logs en Cloud Console
- [ ] Configurar alertas (opcional)
- [ ] Monitorear uso de recursos
- [ ] Verificar costos en Billing

```powershell
# Ver logs en tiempo real
gcloud run services logs tail libreria-joda --region=us-central1

# Ver últimos errores
gcloud run services logs read libreria-joda --region=us-central1 --filter="severity>=ERROR" --limit=50
```

## 🔄 ACTUALIZACIONES FUTURAS

### Para actualizar la aplicación:
```powershell
# 1. Hacer cambios en código local
# 2. Probar localmente
# 3. Hacer backup de datos (si hay cambios en DB)
python exportar_datos.py

# 4. Desplegar nueva versión
.\deploy.ps1

# 5. Verificar que todo funciona
# 6. Si hay problemas, hacer rollback:
gcloud run services update-traffic libreria-joda `
    --region=us-central1 `
    --to-revisions=REVISION_ANTERIOR=100
```

## 🆘 SOLUCIÓN DE PROBLEMAS

### Datos no persisten
- [ ] Verificar que Cloud SQL está configurado
- [ ] Verificar variables de entorno
- [ ] Revisar logs de conexión a BD

### Aplicación no responde (502/503)
- [ ] Revisar logs de Cloud Run
- [ ] Verificar que Dockerfile es correcto
- [ ] Verificar dependencies en requirements.txt
- [ ] Aumentar timeout y memoria

### Error de autenticación
- [ ] Re-autenticar: `firebase login --reauth`
- [ ] Re-autenticar GCloud: `gcloud auth login`
- [ ] Verificar permisos en IAM

### Costos inesperados
- [ ] Revisar console de Billing
- [ ] Configurar alertas de presupuesto
- [ ] Reducir min-instances a 0
- [ ] Verificar que no hay recursos huérfanos

## 📞 RECURSOS DE AYUDA

- Firebase Console: https://console.firebase.google.com
- Google Cloud Console: https://console.cloud.google.com
- Documentación Firebase: https://firebase.google.com/docs
- Documentación Cloud Run: https://cloud.google.com/run/docs

## ✅ CHECKLIST FINAL

- [ ] Aplicación desplegada y accesible
- [ ] Datos respaldados e importados
- [ ] Base de datos persistente configurada
- [ ] Variables de entorno seguras configuradas
- [ ] Monitoreo y logs revisados
- [ ] Costos monitoreados
- [ ] Documentación leída y entendida
- [ ] Backup regular planificado

## 🎉 ¡LISTO!

Si completaste todos los items de este checklist, tu aplicación está:
- ✅ Desplegada en producción
- ✅ Con datos persistentes
- ✅ Segura
- ✅ Monitoreable
- ✅ Lista para usuarios reales

---

**Próximos pasos recomendados:**

1. Configurar dominio personalizado
2. Configurar CI/CD con GitHub Actions
3. Configurar backups automáticos
4. Implementar monitoreo con alertas
5. Optimizar rendimiento y costos
