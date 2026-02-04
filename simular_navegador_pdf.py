#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulación exacta de descarga de PDF desde navegador
"""

import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5001"
USERNAME = "admin"
PASSWORD = "admin123"

def simular_descarga_navegador():
    """Simula exactamente lo que hace el navegador"""
    session = requests.Session()
    
    # Headers típicos del navegador
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    print("🌐 1. Simulando navegador web...")
    
    # 1. Ir a la página principal
    response = session.get(BASE_URL)
    print(f"   📍 Página principal: {response.status_code}")
    
    # 2. Ir al login
    response = session.get(f"{BASE_URL}/auth/login")
    print(f"   🔐 Página login: {response.status_code}")
    
    # 3. Hacer login
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=True)
    print(f"   ✅ Login: {response.status_code}")
    
    # 4. Ir a facturas
    response = session.get(f"{BASE_URL}/invoices")
    print(f"   📄 Página facturas: {response.status_code}")
    
    # 5. Obtener facturas
    response = session.get(f"{BASE_URL}/invoices/api/invoices")
    facturas = response.json()
    print(f"   📋 Facturas obtenidas: {len(facturas)}")
    
    if facturas:
        # 6. Descargar PDF de la primera factura
        invoice_id = facturas[0]['id']
        print(f"\n📱 2. Descargando PDF de factura {invoice_id}...")
        
        # Cambiar headers para descarga de PDF
        session.headers.update({
            'Accept': 'application/pdf,*/*',
        })
        
        pdf_url = f"{BASE_URL}/invoices/api/invoices/{invoice_id}/pdf"
        print(f"   🔗 URL: {pdf_url}")
        
        response = session.get(pdf_url, stream=True)
        
        print(f"   📊 Status: {response.status_code}")
        print(f"   📊 Content-Type: {response.headers.get('Content-Type')}")
        print(f"   📊 Content-Disposition: {response.headers.get('Content-Disposition')}")
        print(f"   📊 Content-Length: {response.headers.get('Content-Length')}")
        
        if response.status_code == 200:
            content = response.content
            print(f"   📦 Tamaño recibido: {len(content)} bytes")
            
            # Verificar si es PDF válido
            if content.startswith(b'%PDF'):
                print("   ✅ PDF válido recibido")
                
                # Guardar archivo
                filename = f"navegador_factura_{invoice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                with open(filename, 'wb') as f:
                    f.write(content)
                print(f"   💾 Guardado como: {filename}")
                
                # Verificar contenido del PDF
                print(f"\n🔍 3. Analizando contenido del PDF...")
                print(f"   📝 Primeros 50 bytes: {content[:50]}")
                print(f"   📝 Últimos 50 bytes: {content[-50:]}")
                
                # Buscar posibles códigos o errores en el PDF
                if b'error' in content.lower() or b'exception' in content.lower():
                    print("   ⚠️  POSIBLE ERROR EN EL CONTENIDO")
                    
                    # Extraer texto legible
                    try:
                        text_content = content.decode('utf-8', errors='ignore')
                        print("   🔍 Contenido como texto:")
                        print(text_content[:500])
                    except:
                        print("   🔍 No se puede decodificar como texto")
                else:
                    print("   ✅ PDF parece normal (sin errores obvios)")
                    
            else:
                print("   ❌ El contenido NO es un PDF válido")
                print(f"   🔍 Primeros 200 bytes: {content[:200]}")
                
                # Intentar decodificar como texto
                try:
                    text_content = content.decode('utf-8')
                    print("   📝 Contenido como texto:")
                    print(text_content)
                except:
                    print("   🔍 No se puede decodificar como texto UTF-8")
                    try:
                        text_content = content.decode('latin-1')
                        print("   📝 Contenido como texto (latin-1):")
                        print(text_content)
                    except:
                        print("   🔍 No se puede decodificar el contenido")
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text[:300]}")

if __name__ == "__main__":
    simular_descarga_navegador()