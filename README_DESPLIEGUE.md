# 🚀 Despliegue de Librería JODA - 100% Gratuito

Sistema de gestión empresarial desplegado con **Firebase Hosting** + **Render.com** (sin costos).

## 📋 Requisitos

- Cuenta de GitHub (gratis)
- Cuenta de Firebase (gratis)
- Cuenta de Render.com (gratis, sin tarjeta)

## ✅ Ventajas de esta Configuración

### Firebase Hosting (Frontend)
- ✅ **100% Gratuito** - 10 GB/mes
- ✅ CDN global (carga rápida en todo el mundo)
- ✅ SSL/HTTPS automático
- ✅ Dominio gratis: `libreria-joda.web.app`

### Render.com (Backend)
- ✅ **100% Gratuito** - 750 horas/mes
- ✅ Sin tarjeta de crédito
- ✅ SSL/HTTPS automático
- ✅ Despliegue automático desde GitHub
- ✅ Python 3.11 + Flask soportado

### Comparación con Google Cloud

| Servicio | Google Cloud Run | Render.com |
|----------|------------------|------------|
| **Costo** | Requiere tarjeta | **Gratis sin tarjeta** |
| **Setup** | Complejo (billing) | **Simple (1 click)** |
| **SSL** | Incluido | **Incluido** |
| **Límites** | 2M requests/mes | 750 horas/mes |
| **Base de datos** | Cloud SQL ($$$) | **PostgreSQL gratis** |

## 🚀 Despliegue Rápido

### Paso 1: Desplegar Frontend en Firebase

```powershell
.\deploy_firebase_gratis.ps1
```

Este script:
1. ✅ Crea backup de datos
2. ✅ Prepara archivos estáticos
3. ✅ Despliega en Firebase Hosting
4. ✅ Genera guía para backend

### Paso 2: Subir Código a GitHub

```bash
git init
git add .
git commit -m "Initial commit - Librería JODA"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/libreria-joda.git
git push -u origin main
```

### Paso 3: Desplegar Backend en Render

1. Ve a [dashboard.render.com/register](https://dashboard.render.com/register)
2. Regístrate con GitHub
3. Click "New +" → "Web Service"
4. Selecciona tu repositorio `libreria-joda`
5. Configuración:
   - **Name:** libreria-joda
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 1 -b 0.0.0.0:$PORT run:app`
   - **Plan:** Free
6. Click "Create Web Service"

### Paso 4: Conectar Firebase con Render

Una vez desplegado en Render, obtendrás una URL como:
```
https://libreria-joda.onrender.com
```

Actualiza `firebase.json`:

```json
{
  "hosting": {
    "public": "public",
    "rewrites": [{
      "source": "/**",
      "destination": "https://libreria-joda.onrender.com"
    }]
  }
}
```

Vuelve a desplegar:

```powershell
firebase deploy --only hosting
```

## 🎯 Acceso Final

- **URL:** https://libreria-joda.web.app
- **Usuario:** admin
- **Contraseña:** admin123

## 📊 Importar Datos

1. Accede a tu sistema en línea
2. Ve a **Configuración** → **Importar Datos**
3. Sube el archivo `datos_backup_YYYYMMDD_HHMMSS.json`
4. ¡Listo! Todos tus productos, ventas y clientes estarán disponibles

## ⚡ Limitaciones del Plan Gratuito

### Render.com Free Tier
- **Sleep después de 15 min:** Primera carga puede tardar 30-60 seg
- **Solución:** Usa [UptimeRobot](https://uptimerobot.com) para hacer ping cada 5 min

### Base de Datos
- **SQLite:** Se reinicia con cada deploy (no persistente)
- **Solución:** Usa PostgreSQL gratuito de Render:
  1. En Render Dashboard → "New +" → "PostgreSQL"
  2. Plan Free (1 GB, persistente)
  3. Copia la DATABASE_URL
  4. Agrega a variables de entorno en tu Web Service

## 🔧 Variables de Entorno en Render

En tu Web Service → Environment:

```
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_aleatoria_aqui
DATABASE_URL=postgresql://... (si usas PostgreSQL)
```

## 📱 Acceso Multiplataforma

Una vez desplegado, accede desde:
- ✅ PC (cualquier navegador)
- ✅ Tablets (Chrome, Safari)
- ✅ Smartphones (iOS, Android)
- ✅ Sin instalación necesaria

## 🛠️ Actualizaciones

Cada vez que hagas cambios en tu código:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

Render automáticamente detectará los cambios y redesplegaráN.

## 📚 Recursos

- [Documentación Render - Deploy Flask](https://render.com/docs/deploy-flask)
- [Firebase Hosting Docs](https://firebase.google.com/docs/hosting)
- [Guía PostgreSQL en Render](https://render.com/docs/databases)

## ❓ Solución de Problemas

### "Application Error" en Render
- Verifica los logs en Render Dashboard
- Asegúrate de que `requirements.txt` incluya `gunicorn`
- Confirma que el comando de inicio sea correcto

### Base de datos vacía después de deploy
- Usa PostgreSQL en lugar de SQLite
- O importa datos después de cada deploy

### Firebase muestra página en blanco
- Verifica que la URL en `firebase.json` sea correcta
- Asegúrate de que el backend en Render esté running

## 💡 Tips

1. **Mantener activo:** Usa UptimeRobot con monitor HTTP cada 5 min
2. **Base datos persistente:** Cambia a PostgreSQL de Render (gratis)
3. **Dominio personalizado:** Render y Firebase permiten custom domains
4. **Backups automáticos:** Programa exports semanales de datos

---

**¿Preguntas?** Abre un issue en GitHub o contacta al soporte de Render.
