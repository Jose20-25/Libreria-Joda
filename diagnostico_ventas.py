#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico específico de ventas
"""

import requests
import json

def diagnostico_ventas():
    """Diagnóstico detallado del sistema de ventas"""
    print("🔍 DIAGNÓSTICO DE VENTAS")
    print("=" * 30)
    
    session = requests.Session()
    
    # 1. Login
    print("🔐 1. Probando login...")
    try:
        response = session.post("http://127.0.0.1:5001/auth/login", 
                              data={'username': 'admin', 'password': 'admin123'}, 
                              allow_redirects=True)
        if response.status_code == 200:
            print("   ✅ Login exitoso")
        else:
            print(f"   ❌ Error en login: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 2. Verificar página de ventas
    print("\n📄 2. Probando página de ventas...")
    try:
        response = session.get("http://127.0.0.1:5001/sales")
        if response.status_code == 200:
            print("   ✅ Página de ventas carga correctamente")
        else:
            print(f"   ❌ Error al cargar página: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Obtener productos disponibles
    print("\n📦 3. Verificando productos disponibles...")
    try:
        # Primero obtener todos los productos
        response = session.get("http://127.0.0.1:5001/inventory/api/products")
        if response.status_code == 200:
            products = response.json()
            available_products = [p for p in products if p.get('stock', 0) > 0 and p.get('active', False)]
            print(f"   📋 {len(products)} productos total")
            print(f"   ✅ {len(available_products)} productos con stock")
            
            if available_products:
                test_product = available_products[0]
                print(f"   🧪 Producto de prueba: {test_product['name']} (ID: {test_product['id']}, Stock: {test_product['stock']})")
                return test_product
            else:
                print("   ❌ No hay productos con stock disponible")
                return None
        else:
            print(f"   ❌ Error al obtener productos: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def probar_venta(session, product):
    """Prueba crear una venta con un producto específico"""
    print(f"\n🛒 4. Probando crear venta...")
    
    venta_data = {
        "customer_name": "Test Cliente",
        "payment_method": "cash",
        "items": [
            {
                "product_id": product['id'],
                "quantity": 1
            }
        ]
    }
    
    print(f"   📝 Datos de venta: {json.dumps(venta_data, indent=2)}")
    
    try:
        response = session.post("http://127.0.0.1:5001/sales/api/sales", 
                              json=venta_data,
                              headers={'Content-Type': 'application/json'})
        
        print(f"   📊 Status Code: {response.status_code}")
        print(f"   📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            result = response.json()
            print("   ✅ Venta creada exitosamente")
            print(f"   📄 Venta: {result.get('sale', {}).get('sale_number', 'N/A')}")
            print(f"   📋 Factura: {result.get('invoice', {}).get('invoice_number', 'N/A')}")
            return True
        else:
            print(f"   ❌ Error HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   📝 Respuesta JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   📝 Respuesta texto: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error de excepción: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    session = requests.Session()
    
    # Login
    response = session.post("http://127.0.0.1:5001/auth/login", 
                          data={'username': 'admin', 'password': 'admin123'}, 
                          allow_redirects=True)
    
    if response.status_code != 200:
        print("❌ No se pudo hacer login")
        return
    
    # Obtener producto de prueba
    product = diagnostico_ventas()
    
    if product:
        # Probar venta
        success = probar_venta(session, product)
        
        if success:
            print(f"\n🎉 DIAGNÓSTICO EXITOSO - El sistema funciona correctamente")
        else:
            print(f"\n❌ PROBLEMA DETECTADO - Revisar logs del servidor")
    else:
        print(f"\n⚠️  No hay productos disponibles para probar")

if __name__ == "__main__":
    main()