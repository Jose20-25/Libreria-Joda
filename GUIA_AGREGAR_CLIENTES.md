# 📋 Guía: Cómo Agregar Nuevos Clientes

## 🎯 Acceso a la Funcionalidad

1. **Iniciar la aplicación:**
   - Ejecutar: `python run.py` o usar `Iniciar_Sistema.bat`
   - Abrir navegador en: `http://127.0.0.1:5001`

2. **Navegar a Clientes:**
   - Hacer clic en "Clientes" en el menú lateral
   - O ir directamente a: `http://127.0.0.1:5001/customers`

## ➕ Agregar Nuevo Cliente

### Pasos para Crear un Cliente:

1. **Abrir formulario:**
   - Hacer clic en el botón **"Nuevo Cliente"** (azul con ícono +)
   - Se abrirá un modal con el formulario

2. **Llenar información básica:**
   - **Nombre Completo** ⭐ (Campo obligatorio)
   - **Teléfono** (10 dígitos recomendado)
   - **Email** (formato válido)
   - **RFC** (máximo 13 caracteres)

3. **Seleccionar tipo de cliente:**
   - **Regular**: Cliente estándar
   - **VIP**: Cliente preferencial con beneficios especiales

4. **Información de ubicación:**
   - **Dirección**: Domicilio completo
   - **Ciudad**: Ciudad de residencia
   - **Estado**: Estado o provincia
   - **Código Postal**: CP de 5 dígitos

5. **Notas adicionales:**
   - Campo libre para observaciones especiales
   - Preferencias del cliente
   - Historial relevante

6. **Guardar cliente:**
   - Hacer clic en **"Guardar Cliente"**
   - Aparecerá notificación de éxito
   - El modal se cerrará automáticamente
   - La tabla se actualizará con el nuevo cliente

## ✏️ Editar Cliente Existente

1. **Localizar cliente:**
   - Usar la barra de búsqueda para encontrar al cliente
   - Busca por nombre, teléfono, RFC, etc.

2. **Editar:**
   - Hacer clic en el ícono de **lápiz** (editar) en la fila del cliente
   - El modal se abrirá con los datos actuales precargados
   - Modificar los campos necesarios
   - Hacer clic en **"Guardar Cliente"**

## 🗑️ Eliminar Cliente

1. **Confirmar eliminación:**
   - Hacer clic en el ícono de **basura** (rojo) en la fila del cliente
   - Confirmar en el diálogo de confirmación
   - El cliente se desactivará (no se elimina físicamente)

## 🔍 Funcionalidades Adicionales

### Búsqueda Inteligente:
- **Campo de búsqueda** en la parte superior de la tabla
- Busca en tiempo real por:
  - Nombre del cliente
  - Teléfono
  - Email
  - RFC
  - Cualquier campo visible

### Tipos de Cliente:
- **Regular**: Badge verde, cliente estándar
- **VIP**: Badge naranja, cliente preferencial

### Estadísticas:
- **Total Clientes**: Número total de clientes activos
- **Clientes VIP**: Cantidad de clientes VIP
- **Nuevos Este Mes**: Clientes registrados en el mes actual
- **Ticket Promedio**: Promedio de compras por cliente

## ⚠️ Validaciones del Sistema

### Campos Obligatorios:
- ✅ **Nombre Completo** - No puede estar vacío

### Validaciones Automáticas:
- ✅ **Email** - Formato válido (ejemplo@dominio.com)
- ✅ **RFC** - Máximo 13 caracteres
- ✅ **Teléfono** - Formato de teléfono válido
- ✅ **Código Postal** - Formato numérico

### Campos Opcionales:
- Teléfono, Email, RFC, Dirección, Ciudad, Estado, CP, Notas

## 💡 Consejos de Uso

1. **Información completa:**
   - Llenar todos los campos posibles mejora el servicio
   - El RFC es importante para facturación

2. **Tipo VIP:**
   - Usar para clientes frecuentes o de alto volumen
   - Facilita identificación rápida

3. **Notas útiles:**
   - Preferencias de productos
   - Horarios de contacto preferidos
   - Descuentos especiales aplicables
   - Historial de incidencias

4. **Búsqueda eficiente:**
   - Usar nombres parciales para búsquedas rápidas
   - El RFC es único y permite localización exacta

## 🔧 Solución de Problemas

### Si no se guarda el cliente:
1. Verificar que el nombre no esté vacío
2. Verificar formato de email si se proporciona
3. Revisar que el RFC no exceda 13 caracteres
4. Verificar conexión a internet

### Si no aparece en la lista:
1. Refrescar la página (F5)
2. Limpiar el campo de búsqueda
3. Verificar que el cliente no haya sido eliminado

### Si el modal no se abre:
1. Desactivar bloqueadores de pop-ups
2. Refrescar la página
3. Verificar que JavaScript esté habilitado

## 📊 Integración con Otras Funciones

### El cliente creado automáticamente:
- ✅ Aparece en listas de selección para ventas
- ✅ Se puede asociar a facturas
- ✅ Se incluye en reportes de clientes
- ✅ Mantiene historial de compras
- ✅ Se puede usar en el sistema de inventario

---

**¿Necesitas ayuda adicional?**
Contacta al administrador del sistema o revisa la documentación técnica en `/docs/`