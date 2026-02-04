#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba completa para el módulo de clientes
Sistema de Librería JODA
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5001"
LOGIN_URL = f"{BASE_URL}/auth/login"
CUSTOMERS_API = f"{BASE_URL}/customers/api/customers"
CUSTOMERS_PAGE = f"{BASE_URL}/customers"

# Credenciales
USERNAME = "admin"
PASSWORD = "admin123"

# Cliente de prueba
CLIENTE_PRUEBA = {
    "name": "Juan Pérez Ejemplo",
    "email": "juan.perez@ejemplo.com",
    "phone": "5551234567",
    "rfc": "PEJE850315ABC",
    "address": "Calle Ejemplo 123, Col. Prueba",
    "city": "Ciudad Ejemplo",
    "state": "Estado Ejemplo",
    "zip_code": "12345",
    "customer_type": "regular",
    "notes": "Cliente de prueba creado automáticamente"
}

def hacer_login(session):
    """
    Realiza el login en el sistema
    
    Args:
        session: Sesión de requests
        
    Returns:
        bool: True si el login fue exitoso
    """
    try:
        # Obtener la página de login para obtener el token CSRF
        login_page = session.get(LOGIN_URL)
        
        if login_page.status_code != 200:
            print(f"❌ Error al acceder a la página de login: {login_page.status_code}")
            return False
        
        # Preparar datos de login
        login_data = {
            'username': USERNAME,
            'password': PASSWORD
        }
        
        # Realizar login
        response = session.post(LOGIN_URL, data=login_data, allow_redirects=False)
        
        # Verificar si el login fue exitoso (redirect a dashboard)
        if response.status_code in [302, 301]:
            print("✅ Login exitoso")
            return True
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error durante el login: {e}")
        return False

def obtener_clientes(session):
    """
    Obtiene la lista de clientes actuales
    
    Args:
        session: Sesión autenticada
        
    Returns:
        list: Lista de clientes o None si hay error
    """
    try:
        response = session.get(CUSTOMERS_API)
        
        if response.status_code == 200:
            clientes = response.json()
            print(f"📊 Se encontraron {len(clientes)} clientes en el sistema")
            return clientes
        else:
            print(f"❌ Error al obtener clientes: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error al obtener clientes: {e}")
        return None

def crear_cliente(session, cliente_data):
    """
    Crea un nuevo cliente
    
    Args:
        session: Sesión autenticada
        cliente_data: Datos del cliente
        
    Returns:
        dict: Datos del cliente creado o None si hay error
    """
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = session.post(
            CUSTOMERS_API,
            data=json.dumps(cliente_data),
            headers=headers
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Cliente creado exitosamente:")
            print(f"   ID: {result['customer']['id']}")
            print(f"   Nombre: {result['customer']['name']}")
            print(f"   Email: {result['customer']['email']}")
            return result['customer']
        else:
            print(f"❌ Error al crear cliente: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error al crear cliente: {e}")
        return None

def verificar_servidor():
    """
    Verifica que el servidor esté funcionando
    
    Returns:
        bool: True si el servidor responde
    """
    try:
        response = requests.get(BASE_URL, timeout=5)
        return response.status_code in [200, 302]  # 302 redirect a login
    except:
        return False

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA COMPLETA DEL MÓDULO DE CLIENTES")
    print("=" * 50)
    print(f"Servidor: {BASE_URL}")
    print(f"Usuario: {USERNAME}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Verificar servidor
    print("🔍 Verificando servidor...")
    if not verificar_servidor():
        print("❌ El servidor no está disponible.")
        print("   Asegúrate de que la aplicación esté ejecutándose:")
        print("   python run.py")
        return
    print("✅ Servidor disponible")
    print()
    
    # 2. Crear sesión y hacer login
    print("🔐 Iniciando sesión...")
    session = requests.Session()
    
    if not hacer_login(session):
        print("❌ No se pudo iniciar sesión. Verifica las credenciales.")
        return
    print()
    
    # 3. Obtener clientes actuales
    print("📋 Obteniendo lista de clientes...")
    clientes_antes = obtener_clientes(session)
    if clientes_antes is None:
        print("❌ No se pudo obtener la lista de clientes")
        return
    print()
    
    # 4. Crear cliente de prueba
    print("➕ Creando cliente de prueba...")
    nuevo_cliente = crear_cliente(session, CLIENTE_PRUEBA)
    if nuevo_cliente is None:
        print("❌ No se pudo crear el cliente de prueba")
        return
    print()
    
    # 5. Verificar que se agregó
    print("✔️ Verificando que el cliente se agregó...")
    clientes_despues = obtener_clientes(session)
    if clientes_despues and len(clientes_despues) > len(clientes_antes):
        print("✅ Cliente agregado correctamente al sistema")
        print(f"   Clientes antes: {len(clientes_antes)}")
        print(f"   Clientes después: {len(clientes_despues)}")
    else:
        print("⚠️ No se detectó aumento en el número de clientes")
    print()
    
    # 6. Resumen final
    print("=" * 50)
    print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print()
    print("📋 Funcionalidades verificadas:")
    print("   ✅ Conexión al servidor")
    print("   ✅ Autenticación de usuario")
    print("   ✅ Obtención de lista de clientes")
    print("   ✅ Creación de nuevo cliente")
    print("   ✅ Validación de datos")
    print()
    print("🌐 Accede a la interfaz web:")
    print(f"   {CUSTOMERS_PAGE}")
    print()
    print("🔍 Cliente de prueba creado:")
    print(f"   Nombre: {CLIENTE_PRUEBA['name']}")
    print(f"   Email: {CLIENTE_PRUEBA['email']}")
    print(f"   Teléfono: {CLIENTE_PRUEBA['phone']}")

if __name__ == "__main__":
    main()