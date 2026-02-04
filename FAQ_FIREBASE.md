# ❓ PREGUNTAS FRECUENTES - Firebase Hosting

## 🔥 General

### ¿Qué es Firebase Hosting?
Firebase Hosting es un servicio de hosting web rápido y seguro de Google. Sirve tu contenido sobre una CDN global (red de distribución de contenido).

### ¿Por qué usar Firebase + Cloud Run y no solo hosting estático?
Tu aplicación es Flask (Python backend), no es solo HTML/CSS/JS. Necesitas:
- **Firebase Hosting**: Para archivos estáticos (CSS, JS, imágenes)
- **Cloud Run**: Para ejecutar el backend Python Flask

### ¿Cuánto cuesta?
- **Firebase Hosting**: Gratis hasta 10GB de transferencia/mes
- **Cloud Run**: Gratis hasta 2 millones de requests/mes
- **Cloud SQL** (opcional): ~$7-10 USD/mes para base de datos persistente

Para tu caso de uso típico: **$0-10 USD/mes**

---

## 💾 Datos y Base de Datos

### ❓ ¿Voy a perder mis datos al desplegar?
**NO**, si sigues los pasos correctamente:

1. Exporta datos ANTES: `python exportar_datos.py`
2. Despliega la aplicación
3. Importa datos DESPUÉS: `python importar_datos.py datos_backup_*.json`

### ❓ ¿Por qué SQLite no es persistente en Cloud Run?
Cloud Run es **stateless** (sin estado). Cada vez que se reinicia el contenedor:
- Se crea desde cero
- Los archivos (incluida la BD SQLite) desaparecen
- Es por diseño para escalabilidad

**Solución**: Usar Cloud SQL (PostgreSQL) o Firestore.

### ❓ ¿Cada cuánto se reinicia el contenedor?
- Cuando no hay tráfico por ~15 minutos (scale to zero)
- Cuando despliegas nueva versión
- Cuando Google actualiza infraestructura
- Bajo carga alta (scaling)

### ❓ ¿Cómo configuro base de datos persistente?
Ver sección "Base de Datos Persistente" en [CHECKLIST_DESPLIEGUE.md](CHECKLIST_DESPLIEGUE.md) o [INICIO_RAPIDO_DESPLIEGUE.md](INICIO_RAPIDO_DESPLIEGUE.md).

**Opción 1: Cloud SQL** (Recomendado)
```powershell
# Ver guía completa en CHECKLIST_DESPLIEGUE.md
gcloud sql instances create libreria-joda-db --database-version=POSTGRES_14 --tier=db-f1-micro --region=us-central1
```

**Opción 2: Firestore**
Requiere cambiar modelos de SQL a NoSQL (más trabajo).

---

## 🚀 Despliegue

### ❓ ¿Cuánto tarda el primer despliegue?
- Build del container: 2-3 minutos
- Deploy a Cloud Run: 1 minuto
- **Total: 3-5 minutos**

### ❓ ¿Y los despliegues siguientes?
1-2 minutos si no cambiaron dependencias.

### ❓ Error: "firebase: command not found"
Firebase CLI no está instalado:
```powershell
npm install -g firebase-tools
```

### ❓ Error: "gcloud: command not found"
Google Cloud SDK no está instalado. Descarga desde:
https://cloud.google.com/sdk/docs/install

### ❓ Error: "Permission denied" o "Unauthorized"
Vuelve a autenticarte:
```powershell
firebase login --reauth
gcloud auth login
```

### ❓ Error: "Project not found"
Configura el proyecto:
```powershell
gcloud config set project libreria-joda
firebase use libreria-joda
```

### ❓ ¿Puedo hacer rollback si algo sale mal?
Sí, Cloud Run guarda las versiones anteriores:
```powershell
# Ver versiones
gcloud run revisions list --service=libreria-joda --region=us-central1

# Volver a versión anterior
gcloud run services update-traffic libreria-joda --to-revisions=REVISION_ANTERIOR=100 --region=us-central1
```

---

## 🔒 Seguridad

### ❓ ¿Mi aplicación es segura en Firebase?
Por defecto, es tan segura como la configuraste localmente. **Debes**:
1. Cambiar `SECRET_KEY` a una clave segura
2. Configurar `FLASK_ENV=production`
3. Usar HTTPS (automático en Firebase Hosting)
4. Cambiar contraseñas de admin

### ❓ ¿Cómo genero una SECRET_KEY segura?
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Luego configúrala:
```powershell
gcloud run services update libreria-joda --set-env-vars="SECRET_KEY=CLAVE_GENERADA_AQUI" --region=us-central1
```

### ❓ ¿Mis datos de Firebase son visibles en el código?
La configuración de Firebase que proporcionaste es para el **frontend** (cliente):
```javascript
apiKey: "AIzaSyAfW7SxYRSWnrO-fYY-z8nQu9qyLDXRxPk"
```

Esto NO es una vulnerabilidad. Es público y está protegido por:
- Reglas de seguridad de Firebase
- Dominios autorizados
- API restrictions en Google Cloud Console

### ❓ ¿Cómo restrinjo quién puede acceder?
**Opción 1**: Autenticación de la app (ya la tienes con Flask-Login)

**Opción 2**: Hacer Cloud Run privado (solo usuarios autenticados de Google):
```powershell
gcloud run services update libreria-joda --no-allow-unauthenticated --region=us-central1
```

---

## 💰 Costos

### ❓ ¿Cuánto me va a costar realmente?
Para un negocio pequeño/mediano:

**Escenario A: Sin Cloud SQL (solo pruebas)**
- Firebase Hosting: $0
- Cloud Run: $0 (bajo tráfico)
- **Total: $0/mes** ⚠️ Datos no persisten

**Escenario B: Con Cloud SQL (producción)**
- Firebase Hosting: $0
- Cloud Run: $0-2 USD
- Cloud SQL (db-f1-micro): $7-10 USD
- **Total: $7-12 USD/mes** ✅ Datos persisten

### ❓ ¿Hay cargos ocultos?
No, si:
- Mantienes tráfico bajo (~1000 ventas/mes o menos)
- Usas tier más pequeño de Cloud SQL
- No subes archivos grandes a Storage

Configura alertas de presupuesto:
```powershell
# En Google Cloud Console > Billing > Budgets & Alerts
```

### ❓ ¿Cómo reduzco costos?
1. **Min instances = 0**: No paga cuando no hay tráfico
```powershell
gcloud run services update libreria-joda --min-instances=0 --region=us-central1
```

2. **Parar Cloud SQL cuando no uses**:
```powershell
gcloud sql instances patch libreria-joda-db --activation-policy=NEVER
```

3. **Usar Firestore** en vez de Cloud SQL (más barato para tráfico bajo)

---

## 📊 Rendimiento

### ❓ ¿Qué es "Cold Start"?
Cuando no hay tráfico, Cloud Run apaga el contenedor (ahorra dinero). La primera petición después de inactividad:
- Tarda 2-5 segundos (arrancar contenedor)
- Las siguientes son instantáneas

**Solución** (cuesta dinero):
```powershell
# Mantener 1 instancia siempre activa
gcloud run services update libreria-joda --min-instances=1 --region=us-central1
```

### ❓ ¿Mi app será rápida?
Sí, muy rápida:
- Firebase Hosting: CDN global, <100ms
- Cloud Run: Región específica, 100-300ms
- Cold start: Solo la primera petición después de inactividad

### ❓ ¿Soporta muchos usuarios simultáneos?
Sí, Cloud Run escala automáticamente:
- Cada instancia: ~80 requests concurrentes
- Máximo por defecto: 100 instancias
- **Soporte estimado**: Miles de usuarios simultáneos

---

## 🔄 Mantenimiento

### ❓ ¿Cómo actualizo mi aplicación?
1. Modifica código localmente
2. Prueba localmente
3. Exporta datos (por seguridad): `python exportar_datos.py`
4. Despliega: `.\deploy.ps1`
5. Verifica que funciona

### ❓ ¿Cómo hago backup de la base de datos?
**Con SQLite**:
```powershell
python exportar_datos.py
```

**Con Cloud SQL**:
```powershell
# Automático (Google lo hace por ti)
# Manual:
gcloud sql backups create --instance=libreria-joda-db
```

### ❓ ¿Cómo restauro un backup?
**Con SQLite**:
```powershell
python importar_datos.py datos_backup_*.json
```

**Con Cloud SQL**:
```powershell
gcloud sql backups restore BACKUP_ID --backup-instance=libreria-joda-db
```

---

## 🌐 Dominio Personalizado

### ❓ ¿Puedo usar mi propio dominio?
Sí, por ejemplo: `www.libreriajoda.com`

**Pasos**:
1. En Firebase Console > Hosting > Add custom domain
2. Verifica propiedad del dominio
3. Apunta DNS a Firebase
4. Espera propagación (1-24 horas)

### ❓ ¿HTTPS es automático?
Sí, Firebase Hosting configura SSL/HTTPS automáticamente. Gratis.

---

## 🔍 Monitoreo

### ❓ ¿Cómo veo logs de errores?
```powershell
# Tiempo real
gcloud run services logs tail libreria-joda --region=us-central1

# Solo errores
gcloud run services logs read libreria-joda --filter="severity>=ERROR" --limit=50 --region=us-central1
```

### ❓ ¿Cómo veo métricas de uso?
- **Cloud Run**: https://console.cloud.google.com/run/detail/us-central1/libreria-joda
- **Firebase**: https://console.firebase.google.com

Métricas disponibles:
- Requests por segundo
- Latencia promedio
- Errores 4xx/5xx
- Uso de memoria/CPU
- Costos

---

## 🆘 Troubleshooting

### ❓ La aplicación muestra error 502/503
**Posibles causas**:
1. Error en el código
2. Dependencias faltantes
3. Puerto incorrecto
4. Timeout

**Diagnóstico**:
```powershell
gcloud run services logs read libreria-joda --region=us-central1 --limit=50
```

### ❓ No puedo conectarme a la base de datos
**Con Cloud SQL**, verifica:
```powershell
# Variables de entorno configuradas
gcloud run services describe libreria-joda --region=us-central1 --format="value(spec.template.spec.containers[0].env)"

# Conexión Cloud SQL añadida
gcloud run services describe libreria-joda --region=us-central1 --format="value(spec.template.metadata.annotations)"
```

### ❓ Los archivos estáticos (CSS/JS) no cargan
Verifica que:
- Los archivos están en `app/static/`
- Las rutas en HTML son correctas
- Firebase Hosting está desplegado: `firebase deploy --only hosting`

---

## 📱 Acceso

### ❓ ¿Cómo accedo a mi aplicación desplegada?
**URLs disponibles**:
- Firebase Hosting: https://libreria-joda.web.app
- Firebase alternativo: https://libreria-joda.firebaseapp.com
- Cloud Run directo: https://libreria-joda-HASH-uc.a.run.app

### ❓ ¿Funciona en móviles?
Sí, igual que tu app local. Es responsiva si tu HTML/CSS lo es.

---

## 💡 Mejores Prácticas

### ❓ ¿Qué NO debo hacer?
❌ Desplegar sin hacer backup
❌ Usar SQLite en producción sin saber que los datos no persisten
❌ Exponer SECRET_KEY en código
❌ No monitorear costos
❌ No revisar logs de errores

### ❓ ¿Qué SÍ debo hacer?
✅ Hacer backup antes de cada despliegue
✅ Configurar Cloud SQL para producción
✅ Usar variables de entorno para secretos
✅ Configurar alertas de presupuesto
✅ Revisar logs regularmente
✅ Probar localmente antes de desplegar

---

## 📞 Ayuda Adicional

### ¿Dónde encuentro más ayuda?

**Documentación del proyecto**:
- [RESUMEN_FIREBASE.md](RESUMEN_FIREBASE.md) - Inicio rápido visual
- [INICIO_RAPIDO_DESPLIEGUE.md](INICIO_RAPIDO_DESPLIEGUE.md) - Pasos detallados
- [GUIA_DESPLIEGUE_FIREBASE.md](GUIA_DESPLIEGUE_FIREBASE.md) - Guía completa
- [CHECKLIST_DESPLIEGUE.md](CHECKLIST_DESPLIEGUE.md) - Lista de verificación

**Documentación oficial**:
- Firebase: https://firebase.google.com/docs
- Cloud Run: https://cloud.google.com/run/docs
- Cloud SQL: https://cloud.google.com/sql/docs

**Comunidad**:
- Stack Overflow: Tag `firebase-hosting`, `google-cloud-run`
- Firebase Community: https://firebase.google.com/community

---

## ✅ Checklist Rápido

```
□ ¿Hice backup de datos? → python exportar_datos.py
□ ¿Instalé Firebase CLI? → npm install -g firebase-tools
□ ¿Instalé Google Cloud SDK? → cloud.google.com/sdk
□ ¿Me autentiqué? → firebase login && gcloud auth login
□ ¿Verifiqué requisitos? → .\verificar_despliegue.ps1
□ ¿Desplegué? → .\deploy.ps1
□ ¿Restauré datos? → python importar_datos.py
□ ¿Configuré Cloud SQL? → Ver CHECKLIST_DESPLIEGUE.md
□ ¿Cambié SECRET_KEY? → gcloud run services update...
```

---

**¿No encuentras respuesta a tu pregunta?**

Ejecuta el menú interactivo:
```powershell
.\inicio_firebase.ps1
```

O consulta la documentación completa en los archivos MD del proyecto.
