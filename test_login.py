#!/usr/bin/env python
"""
Test directo de login - Simula el proceso de autenticación
"""
from app import create_app, db
from app.models.models import User

app = create_app('development')

with app.app_context():
    print("\n" + "="*60)
    print("TEST DE AUTENTICACION - Simulando Login")
    print("="*60 + "\n")
    
    # Datos de prueba
    username_prueba = "admin"
    password_prueba = "admin123"  # La que acabamos de establecer
    
    print(f"Intentando login con:")
    print(f"  Username: {username_prueba}")
    print(f"  Password: {password_prueba}\n")
    
    # Buscar usuario (igual que en auth.py)
    user = User.query.filter_by(username=username_prueba).first()
    
    if user:
        print(f"✅ Usuario encontrado: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Activo: {user.active}")
        
        # Verificar contraseña (igual que en auth.py)
        if user.check_password(password_prueba):
            print(f"\n✅ Contraseña correcta!")
            print(f"   Login exitoso")
            
            if not user.active:
                print(f"\n⚠️  ADVERTENCIA: Usuario desactivado")
            else:
                print(f"\n✅ Usuario activo - Login permitido")
        else:
            print(f"\n❌ Contraseña incorrecta")
    else:
        print(f"❌ Usuario no encontrado")
    
    # Probar también con username en minúsculas/mayúsculas
    print("\n" + "-"*60)
    print("Probando variaciones de username:")
    print("-"*60)
    
    variaciones = ['admin', 'Admin', 'ADMIN', 'admin ']
    for var in variaciones:
        user_test = User.query.filter_by(username=var).first()
        if user_test:
            pwd_ok = user_test.check_password(password_prueba)
            print(f"  '{var}': Usuario encontrado - Password OK: {pwd_ok}")
        else:
            print(f"  '{var}': Usuario NO encontrado")
    
    print("\n" + "="*60)
    print("CREDENCIALES CORRECTAS PARA LOGIN")
    print("="*60)
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("\n  Asegúrate de escribirlo EXACTAMENTE así")
    print("  (sin espacios antes o después)")
    print("="*60 + "\n")
