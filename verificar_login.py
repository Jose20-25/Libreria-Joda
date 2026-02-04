#!/usr/bin/env python
"""
Verificar y probar login del usuario
"""
from app import create_app, db
from app.models.models import User

app = create_app('development')

with app.app_context():
    print("\n" + "="*60)
    print("VERIFICACION DE USUARIO Y CONTRASEÑA")
    print("="*60 + "\n")
    
    # Buscar usuario admin
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"✅ Usuario encontrado en base de datos")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Rol: {admin.role}")
        print(f"   Activo: {admin.active}")
        print(f"   Password hash: {admin.password_hash[:30]}...")
        
        # Probar contraseña
        print("\n--- Probando Contraseñas ---")
        
        contraseñas_probar = ['123456', 'admin', 'Admin123', '']
        
        for pwd in contraseñas_probar:
            resultado = admin.check_password(pwd)
            emoji = "✅" if resultado else "❌"
            print(f"{emoji} Contraseña '{pwd}': {resultado}")
        
        # Probar con la que debería ser
        print("\n--- Estableciendo Nueva Contraseña ---")
        nueva_pwd = "admin123"
        admin.set_password(nueva_pwd)
        db.session.commit()
        
        print(f"✅ Nueva contraseña establecida: {nueva_pwd}")
        print(f"   Verificando: {admin.check_password(nueva_pwd)}")
        
        print("\n" + "="*60)
        print("CREDENCIALES ACTUALIZADAS")
        print("="*60)
        print(f"  Usuario: {admin.username}")
        print(f"  Contraseña: {nueva_pwd}")
        print(f"  Email: {admin.email}")
        print("\n  URL Local: http://localhost:5001")
        print("="*60 + "\n")
    else:
        print("❌ No se encontró usuario admin")
        print("   Ejecuta: python crear_admin.py")
