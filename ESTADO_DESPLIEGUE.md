# DESPLIEGUE COMPLETADO

## ✅ Estado Actual

### 1. Firebase Hosting
- **Estado:** ✅ Desplegado
- **URL:** https://libreria-joda.web.app
- **Contenido:** Página estática con instrucciones

### 2. Git Repository
- **Estado:** ⏳ Listo para subir
- **Archivos preparados:**
  - ✅ .gitignore configurado
  - ✅ README.md creado
  - ✅ runtime.txt (Python 3.11)
  - ✅ Procfile (Gunicorn)
  - ✅ requirements.txt
  - ✅ render.yaml

### 3. Backend (Render.com)
- **Estado:** ⏳ Pendiente de configuración
- **Requisitos:** Subir código a GitHub primero

## 🚀 Siguientes Pasos

### Paso 1: Inicializar Git y Subir a GitHub

Ejecuta:
```powershell
.\inicializar_git.ps1
```

O manualmente:
```bash
git init
git add .
git commit -m "Initial commit - Sistema ERP Libreria JODA"
git branch -M main
```

Luego crea un repositorio en GitHub:
1. Ve a https://github.com/new
2. Nombre: `libreria-joda`
3. Privado o Público (tu elección)
4. NO inicialices con README
5. Copia la URL del repositorio

Conecta y sube:
```bash
git remote add origin https://github.com/TU_USUARIO/libreria-joda.git
git push -u origin main
```

### Paso 2: Desplegar en Render.com

1. **Registrarse:** https://dashboard.render.com/register
   - Usa tu cuenta de GitHub

2. **Crear Web Service:**
   - Click "New +" → "Web Service"
   - Conecta tu repositorio `libreria-joda`

3. **Configuración:**
   ```
   Name: libreria-joda
   Environment: Python 3
   Region: Oregon
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 1 -b 0.0.0.0:$PORT run:app
   Plan: Free
   ```

4. **Variables de Entorno:**
   ```
   FLASK_ENV = production
   SECRET_KEY = (genera un valor aleatorio largo)
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Espera 5-10 minutos

### Paso 3: Conectar Firebase con Render

Una vez que Render te dé la URL (ej: `https://libreria-joda.onrender.com`):

1. Edita `firebase.json`:
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

2. Redespliega Firebase:
```bash
firebase deploy --only hosting
```

### Paso 4: Importar Datos

1. Ve a https://libreria-joda.web.app
2. Login: `admin` / `admin123`
3. Configuración → Importar Datos
4. Sube: `datos_backup_20260203_171155.json`

## 🎯 Scripts Disponibles

### Despliegue Completo Automatizado
```powershell
.\desplegar_todo.ps1
```
Te guía paso a paso por todo el proceso

### Solo Inicializar Git
```powershell
.\inicializar_git.ps1
```
Prepara Git y abre GitHub

### Solo Firebase
```powershell
.\deploy_gratis.ps1
```
Despliega solo en Firebase Hosting

## 📊 Configuración Actual

### Archivos Creados
- ✅ `runtime.txt` - Versión de Python para Render
- ✅ `Procfile` - Comando de inicio para Render
- ✅ `init_db.sh` - Script de inicialización de BD
- ✅ `README.md` - Documentación completa
- ✅ `inicializar_git.ps1` - Script Git
- ✅ `desplegar_todo.ps1` - Script completo
- ✅ `INSTRUCCIONES_DESPLIEGUE_GRATIS.html` - Guía visual

### Archivos Modificados
- ✅ `config/config.py` - Soporte PostgreSQL + Fix para Render
- ✅ `.gitignore` - Excluir archivos sensibles

## 💡 Tips

### Mantener Activo en Render (Gratis)
Render duerme después de 15 min sin uso. Soluciones:

1. **UptimeRobot** (Recomendado):
   - Regístrate en https://uptimerobot.com
   - Crea monitor HTTP
   - URL: `https://libreria-joda.onrender.com/health`
   - Intervalo: 5 minutos

2. **Cron-Job.org:**
   - Similar a UptimeRobot
   - Gratis, sin registro

### Base de Datos Persistente
SQLite se reinicia en cada deploy. Para datos persistentes:

1. En Render: "New +" → "PostgreSQL"
2. Plan: Free (1 GB)
3. Copia `DATABASE_URL`
4. Agrégala a variables de entorno del Web Service
5. La app detectará automáticamente PostgreSQL

## 🔐 Credenciales

**Sistema:**
- Usuario: `admin`
- Contraseña: `admin123`

**Cambiar contraseña:**
```bash
python configurar_usuario.py
```

## 📞 Recursos

- [Firebase Console](https://console.firebase.google.com/project/libreria-joda)
- [Render Dashboard](https://dashboard.render.com)
- [GitHub](https://github.com)
- [Guía Render + Flask](https://render.com/docs/deploy-flask)

## ✅ Checklist

- [x] Backup de datos creado
- [x] Firebase Hosting desplegado
- [x] Archivos de configuración creados
- [x] Scripts de despliegue listos
- [ ] Código subido a GitHub
- [ ] Backend desplegado en Render
- [ ] Firebase conectado con Render
- [ ] Datos importados

---

**Siguiente acción:** Ejecuta `.\desplegar_todo.ps1` para completar el despliegue
