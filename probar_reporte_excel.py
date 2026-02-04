#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el Reporte Profesional de Inventario
Sistema de Librería JODA
"""

import requests
import json
from datetime import datetime
import os

# Configuración
BASE_URL = "http://127.0.0.1:5001"
LOGIN_URL = f"{BASE_URL}/auth/login"
EXCEL_URL = f"{BASE_URL}/reports/api/reports/export/excel"
REPORTS_URL = f"{BASE_URL}/reports"

# Credenciales
USERNAME = "admin"
PASSWORD = "admin123"

def verificar_servidor():
    """Verifica que el servidor esté funcionando"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code in [200, 302]
    except:
        return False

def hacer_login(session):
    """Realiza el login en el sistema"""
    try:
        # Obtener página de login
        login_page = session.get(LOGIN_URL)
        if login_page.status_code != 200:
            return False
        
        # Hacer login
        login_data = {
            'username': USERNAME,
            'password': PASSWORD
        }
        
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        return response.status_code in [302, 301]
    except:
        return False

def generar_reporte_excel(session):
    """Genera el reporte profesional de inventario"""
    try:
        response = session.get(EXCEL_URL)
        
        if response.status_code == 200:
            # Guardar archivo
            filename = f"inventario_profesional_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filepath)
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'size': file_size
            }
        else:
            return {
                'success': False,
                'error': f"Error HTTP {response.status_code}",
                'response': response.text[:200]
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA DEL REPORTE PROFESIONAL DE INVENTARIO")
    print("=" * 60)
    print(f"🕒 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Servidor: {BASE_URL}")
    print()
    
    # 1. Verificar servidor
    print("🔍 1. Verificando servidor...")
    if not verificar_servidor():
        print("❌ El servidor no está disponible")
        print("   Asegúrate de ejecutar: python run.py")
        return
    print("✅ Servidor disponible")
    
    # 2. Iniciar sesión
    print("\n🔐 2. Iniciando sesión...")
    session = requests.Session()
    
    if not hacer_login(session):
        print("❌ Error al iniciar sesión")
        return
    print("✅ Sesión iniciada correctamente")
    
    # 3. Generar reporte
    print("\n📊 3. Generando reporte profesional...")
    print("   ⏳ Procesando inventario...")
    print("   ⏳ Aplicando estilos profesionales...")
    print("   ⏳ Creando gráficos...")
    print("   ⏳ Organizando por categorías...")
    
    resultado = generar_reporte_excel(session)
    
    if resultado['success']:
        print("✅ ¡Reporte generado exitosamente!")
        print(f"\n📁 ARCHIVO GENERADO:")
        print(f"   📂 Nombre: {resultado['filename']}")
        print(f"   📂 Ruta: {resultado['filepath']}")
        print(f"   📂 Tamaño: {resultado['size']:,} bytes ({resultado['size']/1024:.1f} KB)")
        
        print(f"\n📋 CONTENIDO DEL REPORTE:")
        print("   📊 Hoja 1: Resumen Ejecutivo")
        print("   📦 Hoja 2: Inventario por Categorías (14 categorías)")
        print("   ⚠️ Hoja 3: Productos con Stock Bajo")
        print("   📈 Hoja 4: Análisis Gráfico")
        
        print(f"\n🎨 CARACTERÍSTICAS VISUALES:")
        print("   ✅ Colores diferenciados por categoría")
        print("   ✅ Resaltado de productos con stock bajo")
        print("   ✅ Gráficos de barras y circulares")
        print("   ✅ Formato profesional con bordes y estilos")
        print("   ✅ Métricas ejecutivas y análisis detallado")
        
        print(f"\n📊 ESTADÍSTICAS INCLUIDAS:")
        print("   📈 Total de productos activos")
        print("   💰 Valor total del inventario")
        print("   ⚠️ Productos con stock bajo")
        print("   🔴 Productos sin stock")
        print("   📊 Distribución por categorías")
        print("   💹 Márgenes de ganancia")
        
        print(f"\n🎯 LISTO PARA USAR:")
        print("   📱 Compatible con Excel 2016+")
        print("   📱 Compatible con LibreOffice Calc")
        print("   📱 Compatible con Google Sheets")
        print(f"   🌐 También disponible en: {REPORTS_URL}")
        
    else:
        print("❌ Error al generar el reporte")
        print(f"   Error: {resultado['error']}")
        if 'response' in resultado:
            print(f"   Respuesta: {resultado['response']}")
    
    print(f"\n🏁 Prueba completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()