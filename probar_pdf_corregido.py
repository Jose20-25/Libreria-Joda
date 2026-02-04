#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de descarga de PDF corregido
"""

import requests
from datetime import datetime

def probar_pdf_corregido():
    """Prueba la descarga de PDF después de las correcciones"""
    print("🔧 PROBANDO PDFs CORREGIDOS")
    print("=" * 40)
    
    session = requests.Session()
    
    # Login
    print("🔐 Haciendo login...")
    response = session.post("http://127.0.0.1:5001/auth/login", 
                          data={'username': 'admin', 'password': 'admin123'}, 
                          allow_redirects=True)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.status_code}")
        return
    
    print("✅ Login exitoso")
    
    # Obtener facturas
    response = session.get("http://127.0.0.1:5001/invoices/api/invoices")
    facturas = response.json()
    print(f"📄 {len(facturas)} facturas encontradas")
    
    if not facturas:
        print("❌ No hay facturas para probar")
        return
    
    # Probar primera factura
    invoice_id = facturas[0]['id']
    print(f"\n📱 Descargando PDF de factura {invoice_id}...")
    
    response = session.get(f"http://127.0.0.1:5001/invoices/api/invoices/{invoice_id}/pdf")
    
    print(f"📊 Status: {response.status_code}")
    print(f"📊 Content-Type: {response.headers.get('Content-Type')}")
    print(f"📊 Content-Length: {response.headers.get('Content-Length')}")
    print(f"📊 Tamaño real: {len(response.content)} bytes")
    
    if response.status_code == 200:
        # Verificar que sea PDF válido
        if response.content.startswith(b'%PDF'):
            print("✅ PDF válido generado")
            
            # Guardar archivo para verificación
            filename = f"factura_corregida_{invoice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"💾 PDF guardado: {filename}")
            
            # Verificar contenido (buscar etiquetas HTML que no deberían estar)
            content_str = response.content.decode('latin-1', errors='ignore')
            
            print("\n🔍 VERIFICACIÓN DE CONTENIDO:")
            
            if '<b>' in content_str or '</b>' in content_str:
                print("❌ TODAVÍA HAY ETIQUETAS HTML EN EL PDF")
                print(f"   Etiquetas <b>: {content_str.count('<b>')}")
                print(f"   Etiquetas </b>: {content_str.count('</b>')}")
            else:
                print("✅ No hay etiquetas HTML en el PDF")
            
            # Verificar que contenga información esperada
            if 'LIBRERÍA JODA' in content_str:
                print("✅ Contiene título de empresa")
            else:
                print("❌ No contiene título de empresa")
                
            if facturas[0]['invoice_number'] in content_str:
                print("✅ Contiene número de factura")
            else:
                print("❌ No contiene número de factura")
                
            if 'TOTAL A PAGAR' in content_str:
                print("✅ Contiene totales")
            else:
                print("❌ No contiene totales")
            
            print(f"\n🎉 PDF de {len(response.content)} bytes generado correctamente!")
            
        else:
            print("❌ La respuesta NO es un PDF válido")
            print(f"🔍 Primeros 100 caracteres:")
            try:
                print(response.content[:100].decode('utf-8'))
            except:
                print(response.content[:100])
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        print(f"🔍 Respuesta: {response.text[:300]}")

if __name__ == "__main__":
    probar_pdf_corregido()