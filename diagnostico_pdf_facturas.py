#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico de descarga de PDFs de facturas
Sistema de Librería JODA
"""

import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5001"
LOGIN_URL = f"{BASE_URL}/auth/login"

# Credenciales
USERNAME = "admin"
PASSWORD = "admin123"

def verificar_servidor():
    """Verifica que el servidor esté funcionando"""
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ Servidor funcionando: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Servidor no responde: {e}")
        return False

def hacer_login(session):
    """Realiza el login en el sistema"""
    try:
        # Obtener formulario de login
        response = session.get(LOGIN_URL)
        if response.status_code != 200:
            return False
        
        # Hacer login
        login_data = {
            'username': USERNAME,
            'password': PASSWORD
        }
        
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        
        # Verificar si el login fue exitoso
        if response.status_code in [302, 301] or "dashboard" in response.headers.get('location', ''):
            print("✅ Login exitoso")
            # Seguir la redirección
            session.get(f"{BASE_URL}/dashboard")
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"🔍 Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error al hacer login: {e}")
        return False

def obtener_facturas(session):
    """Obtiene la lista de facturas"""
    try:
        response = session.get(f"{BASE_URL}/invoices/api/invoices")
        if response.status_code == 200:
            facturas = response.json()
            print(f"📄 Facturas encontradas: {len(facturas)}")
            return facturas
        else:
            print(f"❌ Error obteniendo facturas: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def probar_descarga_pdf(session, invoice_id):
    """Prueba la descarga de PDF de una factura"""
    try:
        pdf_url = f"{BASE_URL}/invoices/api/invoices/{invoice_id}/pdf"
        print(f"\n📱 Probando descarga de PDF para factura {invoice_id}")
        print(f"🔗 URL: {pdf_url}")
        
        response = session.get(pdf_url)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Content-Type: {response.headers.get('Content-Type', 'No especificado')}")
        print(f"📊 Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # Verificar si es realmente un PDF
            if response.content.startswith(b'%PDF'):
                print("✅ PDF válido generado")
                
                # Guardar archivo para verificación
                filename = f"test_factura_{invoice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                filepath = os.path.join(os.path.dirname(__file__), filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"💾 PDF guardado: {filename}")
                return True
            else:
                print("❌ La respuesta no es un PDF válido")
                print("🔍 Primeros 500 caracteres de la respuesta:")
                try:
                    print(response.content[:500].decode('utf-8'))
                except:
                    print(response.content[:500])
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print("🔍 Respuesta del servidor:")
            print(response.text[:500])
            return False
            
    except Exception as e:
        print(f"❌ Error al descargar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DE DESCARGA DE PDFs DE FACTURAS")
    print("=" * 50)
    
    # Verificar servidor
    print("\n📡 1. Verificando servidor...")
    if not verificar_servidor():
        return
    
    # Crear sesión
    session = requests.Session()
    
    # Login
    print("\n🔐 2. Realizando login...")
    if not hacer_login(session):
        return
    
    # Obtener facturas
    print("\n📄 3. Obteniendo lista de facturas...")
    facturas = obtener_facturas(session)
    
    if not facturas:
        print("❌ No hay facturas para probar")
        return
    
    # Probar descarga con las primeras 3 facturas
    print("\n📱 4. Probando descarga de PDFs...")
    for i, factura in enumerate(facturas[:3]):
        invoice_id = factura['id']
        success = probar_descarga_pdf(session, invoice_id)
        
        if not success:
            print(f"❌ Fallo en factura {invoice_id}")
            break
    
    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    main()