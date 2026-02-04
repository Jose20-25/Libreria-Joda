#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar/crear usuario administrador
Sistema de Librería JODA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import User
from werkzeug.security import generate_password_hash

def crear_usuario_admin():
    """Crea el usuario administrador si no existe"""
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existe un usuario admin
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("✅ Usuario 'admin' ya existe")
            print(f"   Email: {admin_user.email}")
            print(f"   Activo: {'Sí' if admin_user.active else 'No'}")
            return True
        
        # Crear usuario admin
        try:
            new_admin = User(
                username='admin',
                email='admin@libreriajoda.com',
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin',
                active=True
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   Email: admin@libreriajoda.com")
            return True
            
        except Exception as e:
            print(f"❌ Error al crear usuario administrador: {e}")
            return False

def main():
    """Función principal"""
    print("🔐 Verificación/Creation de Usuario Administrador")
    print("=" * 50)
    
    if crear_usuario_admin():
        print("\n🎉 Sistema listo para usar!")
        print("   Accede en: http://127.0.0.1:5001")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
    else:
        print("\n❌ Error en la configuración del usuario")

if __name__ == "__main__":
    main()