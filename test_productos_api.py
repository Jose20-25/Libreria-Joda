#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar API de productos
"""

import requests

def verificar_api_productos():
    session = requests.Session()
    session.post('http://127.0.0.1:5001/auth/login', data={'username': 'admin', 'password': 'admin123'})
    
    response = session.get('http://127.0.0.1:5001/inventory/api/products')
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        products = response.json()
        with_stock = [p for p in products if p.get('stock', 0) > 0]
        active_products = [p for p in products if p.get('active', False)]
        
        print(f'📊 Total productos: {len(products)}')
        print(f'✅ Productos activos: {len(active_products)}')
        print(f'📦 Productos con stock: {len(with_stock)}')
        
        if with_stock:
            print(f'\n🔝 Ejemplos con stock:')
            for p in with_stock[:3]:
                print(f'   • {p["name"]} - Stock: {p["stock"]} - Activo: {p.get("active", False)}')
        
        return with_stock
    else:
        print(f'❌ Error: {response.text[:200]}')
        return []

if __name__ == "__main__":
    productos = verificar_api_productos()
    
    if productos:
        print(f"\n🧪 Probando venta con producto: {productos[0]['name']}")
        
        session = requests.Session()
        session.post('http://127.0.0.1:5001/auth/login', data={'username': 'admin', 'password': 'admin123'})
        
        venta_data = {
            "customer_name": "Test Cliente",
            "payment_method": "cash", 
            "items": [{"product_id": productos[0]['id'], "quantity": 1}]
        }
        
        response = session.post('http://127.0.0.1:5001/sales/api/sales', json=venta_data)
        print(f"\n📊 Respuesta venta: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Venta procesada correctamente")
            data = response.json()
            print(f"📄 Venta: {data.get('sale', {}).get('sale_number')}")
            print(f"📋 Factura: {data.get('invoice', {}).get('invoice_number')}")
        else:
            print(f"❌ Error: {response.text[:300]}")
    else:
        print("❌ No hay productos disponibles para venta")