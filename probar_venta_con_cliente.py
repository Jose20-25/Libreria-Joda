#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba completa del sistema de ventas con clientes
"""

import requests
import json

def probar_venta_con_cliente():
    session = requests.Session()
    
    # Login
    session.post('http://127.0.0.1:5001/auth/login', data={'username': 'admin', 'password': 'admin123'})
    
    print("🧪 PRUEBA: VENTA CON CLIENTE ESPECÍFICO")
    print("=" * 45)
    
    # Obtener clientes
    customers_response = session.get('http://127.0.0.1:5001/customers/api/customers')
    if customers_response.status_code == 200:
        customers = customers_response.json()
        print(f"👥 Clientes disponibles: {len(customers)}")
        if customers:
            test_customer = customers[0]
            print(f"🧪 Cliente de prueba: {test_customer['name']} (ID: {test_customer['id']})")
        else:
            print("❌ No hay clientes disponibles")
            return
    else:
        print("❌ Error al obtener clientes")
        return
    
    # Obtener producto
    products_response = session.get('http://127.0.0.1:5001/inventory/api/products')
    if products_response.status_code == 200:
        products = [p for p in products_response.json() if p.get('stock', 0) > 0]
        if products:
            test_product = products[0]
            print(f"📦 Producto de prueba: {test_product['name']} (ID: {test_product['id']})")
        else:
            print("❌ No hay productos con stock")
            return
    else:
        print("❌ Error al obtener productos")
        return
    
    # Crear venta con cliente específico
    venta_data = {
        "customer_id": test_customer['id'],
        "customer_name": test_customer['name'],
        "payment_method": "card",
        "items": [{"product_id": test_product['id'], "quantity": 2}]
    }
    
    print(f"\n🛒 Creando venta...")
    print(f"   👤 Cliente: {test_customer['name']}")
    print(f"   📦 Producto: {test_product['name']} x2")
    print(f"   💳 Pago: Tarjeta")
    
    response = session.post('http://127.0.0.1:5001/sales/api/sales', json=venta_data)
    
    if response.status_code == 201:
        result = response.json()
        sale = result['sale']
        invoice = result['invoice']
        
        print(f"\n✅ VENTA EXITOSA")
        print(f"   📄 Venta: {sale['sale_number']}")
        print(f"   📋 Factura: {invoice['invoice_number']}")
        print(f"   👤 Cliente: {sale['customer_name']}")
        print(f"   💰 Total: ${sale['total']:.2f}")
        print(f"   💳 Pago: {sale['payment_method']}")
        
        print(f"\n🎉 Sistema funcionando perfectamente con selección de clientes")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text[:300]}")

if __name__ == "__main__":
    probar_venta_con_cliente()