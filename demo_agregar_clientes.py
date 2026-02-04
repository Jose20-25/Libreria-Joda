#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demostración para agregar clientes de ejemplo
Sistema de Librería JODA
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5001"
CUSTOMERS_ENDPOINT = f"{BASE_URL}/customers/api/customers"

# Clientes de ejemplo para agregar
CLIENTES_EJEMPLO = [
    {
        "name": "María González López",
        "email": "maria.gonzalez@email.com",
        "phone": "5551234567",
        "rfc": "GOLM850315ABC",
        "address": "Av. Juárez 123, Col. Centro",
        "city": "Ciudad de México",
        "state": "CDMX",
        "zip_code": "06000",
        "customer_type": "regular",
        "notes": "Cliente frecuente, prefiere libros de historia"
    },
    {
        "name": "Carlos Ramírez Sánchez",
        "email": "carlos.ramirez@gmail.com",
        "phone": "5559876543",
        "rfc": "RASC920710XYZ",
        "address": "Calle Morelos 456, Col. San Juan",
        "city": "Guadalajara",
        "state": "Jalisco",
        "zip_code": "44100",
        "customer_type": "vip",
        "notes": "Cliente VIP, compras mensuales de material académico"
    },
    {
        "name": "Ana Patricia Herrera",
        "email": "ana.herrera@outlook.com",
        "phone": "5555678901",
        "rfc": "HEPA880425DEF",
        "address": "Blvd. Revolución 789, Col. Industrial",
        "city": "Monterrey",
        "state": "Nuevo León",
        "zip_code": "64000",
        "customer_type": "regular",
        "notes": "Profesora de primaria, compra libros infantiles"
    },
    {
        "name": "Roberto Mendoza Cruz",
        "email": "roberto.mendoza@yahoo.com",
        "phone": "5553456789",
        "rfc": "MECR750620GHI",
        "address": "Av. Insurgentes 321, Col. Roma",
        "city": "Ciudad de México",
        "state": "CDMX",
        "zip_code": "06700",
        "customer_type": "vip",
        "notes": "Coleccionista de libros raros, presupuesto alto"
    },
    {
        "name": "Laura Jiménez Torres",
        "email": "laura.jimenez@hotmail.com",
        "phone": "5557890123",
        "rfc": "JITL900515JKL",
        "address": "Calle Hidalgo 654, Col. Centro Histórico",
        "city": "Puebla",
        "state": "Puebla",
        "zip_code": "72000",
        "customer_type": "regular",
        "notes": "Estudiante universitaria, compra libros de texto"
    }
]

def agregar_cliente(cliente_data):
    """
    Agrega un cliente usando la API del sistema
    
    Args:
        cliente_data (dict): Datos del cliente a agregar
        
    Returns:
        bool: True si se agregó exitosamente, False en caso contrario
    """
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            CUSTOMERS_ENDPOINT, 
            data=json.dumps(cliente_data), 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Cliente agregado: {cliente_data['name']}")
            print(f"   ID: {result['customer']['id']}")
            return True
        else:
            print(f"❌ Error al agregar {cliente_data['name']}: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión al agregar {cliente_data['name']}: {e}")
        return False

def verificar_conexion():
    """
    Verifica que el servidor esté funcionando
    
    Returns:
        bool: True si el servidor responde, False en caso contrario
    """
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Función principal del script"""
    print("🚀 Script de Demostración - Agregar Clientes")
    print("=" * 50)
    print(f"Servidor: {BASE_URL}")
    print(f"Endpoint: {CUSTOMERS_ENDPOINT}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar conexión
    print("🔍 Verificando conexión al servidor...")
    if not verificar_conexion():
        print("❌ No se puede conectar al servidor.")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://127.0.0.1:5001")
        return
    
    print("✅ Conexión exitosa al servidor")
    print()
    
    # Agregar clientes de ejemplo
    print("📋 Agregando clientes de ejemplo...")
    print()
    
    exitosos = 0
    fallidos = 0
    
    for i, cliente in enumerate(CLIENTES_EJEMPLO, 1):
        print(f"Cliente {i}/{len(CLIENTES_EJEMPLO)}: {cliente['name']}")
        
        if agregar_cliente(cliente):
            exitosos += 1
        else:
            fallidos += 1
        
        print()
    
    # Resumen
    print("=" * 50)
    print("📊 RESUMEN:")
    print(f"✅ Clientes agregados exitosamente: {exitosos}")
    print(f"❌ Errores: {fallidos}")
    print(f"📈 Total procesados: {len(CLIENTES_EJEMPLO)}")
    
    if exitosos > 0:
        print()
        print("🎉 Los clientes se han agregado al sistema.")
        print("   Puedes verlos en: http://127.0.0.1:5001/customers")
    
    print()
    print("🏁 Script completado.")

if __name__ == "__main__":
    main()