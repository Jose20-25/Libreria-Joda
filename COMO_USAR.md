# 🏪 Sistema ERP - Librería JODA

Sistema de gestión empresarial completo para librería, desarrollado con Python Flask.

## 🚀 Formas de Iniciar el Sistema

### Opción 1: Archivo BAT (Más Simple)
1. Haz doble clic en `Iniciar_Sistema.bat`
2. El servidor se iniciará automáticamente
3. El navegador se abrirá en http://127.0.0.1:5001

### Opción 2: Launcher de Python
1. Ejecuta: `python launcher.py`
2. El sistema iniciará y abrirá el navegador automáticamente

### Opción 3: Crear Ejecutable (Opcional)
1. Ejecuta: `python build_exe.py`
2. Espera a que se cree el ejecutable
3. Copia `dist/Libreria_JODA_ERP.exe` al directorio raíz
4. Haz doble clic en el .exe para iniciar

### Opción 4: Manual
1. Abre una terminal en el directorio del proyecto
2. Ejecuta: `python run.py`
3. Abre tu navegador en http://127.0.0.1:5001

## 📋 Requisitos Previos

- Python 3.11 o superior
- Dependencias instaladas: `pip install -r requirements.txt`

## 🔑 Acceso al Sistema

**Usuario por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📦 Módulos del Sistema

1. **Dashboard** - Vista general con estadísticas
2. **Inventario** - Gestión de productos por categorías
3. **Ventas** - Punto de venta con filtros por categoría
4. **Compras** - Órdenes de compra y recepción
5. **Clientes** - Gestión de clientes VIP/Regular
6. **Facturas** - Generación de facturas con PDF profesional
7. **Reportes** - Gráficas y exportación a Excel
8. **Configuración** - Ajustes del sistema (IVA 13%)

## 💡 Características Principales

✅ IVA 13% incluido en precios
✅ Organización por 14 categorías de productos
✅ Generación de PDF profesional para facturas
✅ Exportación de reportes a Excel
✅ Búsqueda y filtros avanzados
✅ Historial de ventas y compras
✅ Gestión de inventario en tiempo real
✅ Interfaz moderna y responsiva

## 🛠️ Solución de Problemas

### El puerto 5001 está en uso
- Cierra otras instancias del servidor
- O cambia el puerto en `run.py`

### El navegador no se abre automáticamente
- Abre manualmente: http://127.0.0.1:5001

### Error de dependencias
- Ejecuta: `pip install -r requirements.txt`

### Error de base de datos
- Elimina `instance/libreria.db` y reinicia
- Se creará una nueva con datos de ejemplo

## 📧 Soporte

Para soporte o consultas sobre el sistema, contacta al administrador.

---
**Librería JODA** - Sistema ERP © 2025
