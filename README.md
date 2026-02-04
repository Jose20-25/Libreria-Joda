# 🏪 LIBRERÍA JODA - Sistema ERP

Sistema ERP completo desarrollado con Flask, SQLAlchemy y tecnologías web modernas para la gestión integral de una librería de útiles escolares.

## ⚡ INICIO RÁPIDO

### ✅ Método Más Simple: Haz doble clic en `Iniciar_Sistema.bat`

Esto iniciará automáticamente:
- ✓ El servidor Flask
- ✓ Tu navegador predeterminado  
- ✓ La página de inicio de sesión

### � Credenciales de Acceso

```
Usuario:    admin
Contraseña: admin123
```

---

## �🚀 Características del Sistema

- **Dashboard Interactivo**: Estadísticas en tiempo real, gráficos y métricas clave
- **Gestión de Inventario**: Control completo de productos con 14 categorías de útiles escolares
- **Punto de Venta (POS)**: Sistema de ventas con carrito, filtros por categoría y búsqueda
- **Gestión de Compras**: Órdenes de compra a proveedores y recepción de mercancía
- **CRM de Clientes**: Base de datos de clientes VIP/Regular con historial
- **Facturación**: Generación de facturas con PDF profesional y logo
- **Reportes**: Gráficas interactivas y exportación a Excel
- **Configuración**: Gestión de IVA (13% incluido) y datos de empresa
- **Autenticación**: Sistema de login seguro con gestión de sesiones

## 📋 Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

## 🔧 Instalación

### 1. Instalar Python (si no está instalado)

Descarga Python desde [python.org](https://www.python.org/downloads/) y asegúrate de marcar "Add Python to PATH" durante la instalación.

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (Opcional)

El archivo `.env` ya está creado con la configuración por defecto. Puedes modificarlo si lo necesitas.

## 🚀 Ejecución

### Inicializar la base de datos (solo la primera vez)

```powershell
python run.py
```

La aplicación creará automáticamente la base de datos y datos de ejemplo al iniciar por primera vez.

### Iniciar el servidor

```powershell
python run.py
```

El servidor se iniciará en: http://localhost:5000

## 👤 Credenciales de Acceso

**Usuario de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📁 Estructura del Proyecto

```
Libreria JODA/
├── app/
│   ├── __init__.py              # Configuración de la aplicación Flask
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py            # Modelos: User, Product, Customer
│   │   ├── transactions.py      # Modelos: Sale, Purchase, Invoice
│   │   └── seed.py              # Datos de ejemplo
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Rutas de autenticación
│   │   ├── main.py              # Dashboard principal
│   │   ├── inventory.py         # Gestión de inventario
│   │   ├── sales.py             # Punto de venta
│   │   ├── purchases.py         # Gestión de compras
│   │   ├── customers.py         # CRM de clientes
│   │   ├── invoices.py          # Facturación
│   │   └── reports.py           # Reportes y exportación
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css         # Estilos principales
│   │   ├── js/
│   │   │   └── main.js          # JavaScript global
│   │   └── logo/
│   │       └── logo.png         # Logo de la empresa
│   └── templates/
│       ├── base.html            # Template base
│       ├── dashboard.html       # Dashboard principal
│       └── auth/
│           └── login.html       # Página de login
├── config/
│   └── config.py                # Configuraciones
├── .env                         # Variables de entorno
├── requirements.txt             # Dependencias de Python
├── run.py                       # Punto de entrada
└── README.md                    # Este archivo
```

## 🔌 API Endpoints

### Inventario
- `GET /inventory/` - Página de inventario
- `GET /inventory/api/products` - Obtener productos
- `POST /inventory/api/products` - Crear producto
- `PUT /inventory/api/products/<id>` - Actualizar producto
- `DELETE /inventory/api/products/<id>` - Eliminar producto

### Ventas
- `GET /sales/` - Página de punto de venta
- `GET /sales/api/sales` - Obtener ventas
- `POST /sales/api/sales` - Crear venta

### Compras
- `GET /purchases/` - Página de compras
- `GET /purchases/api/purchases` - Obtener órdenes
- `POST /purchases/api/purchases` - Crear orden
- `POST /purchases/api/purchases/<id>/receive` - Recibir orden

### Clientes
- `GET /customers/` - Página de clientes
- `GET /customers/api/customers` - Obtener clientes
- `POST /customers/api/customers` - Crear cliente
- `PUT /customers/api/customers/<id>` - Actualizar cliente

### Facturas
- `GET /invoices/` - Página de facturación
- `GET /invoices/api/invoices` - Obtener facturas
- `POST /invoices/api/invoices` - Crear factura

### Reportes
- `GET /reports/` - Página de reportes
- `GET /reports/api/reports/dashboard` - Datos del dashboard
- `GET /reports/api/reports/export/excel` - Exportar a Excel

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones
- **SQLite** - Base de datos
- **OpenPyXL** - Generación de archivos Excel
- **ReportLab** - Generación de PDFs

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos con diseño moderno
- **JavaScript ES6+** - Interactividad
- **Chart.js** - Gráficos interactivos
- **Font Awesome** - Iconos

## 📊 Funcionalidades Principales

### 1. Inventario
- 14 categorías predefinidas de útiles escolares
- Generación automática de códigos por categoría
- Control de stock mínimo
- Alertas de productos con stock bajo
- Búsqueda y filtros avanzados

### 2. Punto de Venta
- Interfaz intuitiva estilo POS
- Carrito de compras dinámico
- Múltiples métodos de pago
- Actualización automática de inventario
- Cálculo automático de IVA (16%)

### 3. Compras
- Órdenes de compra a proveedores
- Estados: Pendiente, Recibida, Cancelada
- Recepción de mercancía con actualización de stock
- Historial completo de compras

### 4. Clientes
- Base de datos completa
- Tipos: Regular y VIP
- Historial de compras por cliente
- Estadísticas de compra

### 5. Facturación
- Generación de facturas con número único
- Cálculo automático de impuestos
- Estados: Pagada, Pendiente, Cancelada
- Exportación a PDF

### 6. Reportes
- Dashboard con métricas clave
- Gráficos de ventas
- Exportación a Excel con formato profesional
- Análisis por categoría y producto

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección de rutas con `@login_required`
- Validación de sesiones
- Sanitización de entradas

## 🎨 Personalización

### Cambiar el nombre de la empresa

Edita el archivo `config/config.py` o actualiza desde la interfaz de Configuración.

### Agregar más categorías

Edita la lista `CATEGORIES` en `app/routes/inventory.py`.

### Modificar el IVA

Actualiza el valor en la base de datos desde Configuración o edita el modelo `SystemConfig`.

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```powershell
pip install -r requirements.txt
```

### Error: "Unable to open database file"
```powershell
# Asegúrate de tener permisos de escritura en la carpeta
# La base de datos se creará automáticamente
```

### El servidor no inicia
```powershell
# Verifica que el puerto 5000 no esté en uso
# Cambia el puerto en run.py si es necesario
```

## 📝 Próximas Mejoras

- [ ] Reportes en PDF
- [ ] Sistema de roles y permisos
- [ ] Respaldo automático de base de datos
- [ ] Notificaciones por email
- [ ] Integración con lectores de código de barras
- [ ] App móvil
- [ ] Multi-tienda
- [ ] Inventario por lotes

## 👥 Soporte

Para soporte, abre un issue en el repositorio o contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto es privado y propietario de LIBRERÍA JODA.

---

**Desarrollado con ❤️ para LIBRERÍA JODA**
