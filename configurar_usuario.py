#!/usr/bin/env python
"""
Configurar o cambiar contraseña del usuario administrador
Version simplificada para PowerShell
"""
from app import create_app, db
from app.models.models import User

def configurar_admin():
    """Configurar usuario administrador"""
    app = create_app('development')
    
    with app.app_context():
        print("\n" + "="*60)
        print("CONFIGURACION DE USUARIO ADMINISTRADOR - Libreria JODA")
        print("="*60 + "\n")
        
        # Buscar usuario admin existente
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print(f"Usuario encontrado: {admin.username}")
            print(f"Email: {admin.email}")
            print(f"Rol: {admin.role}\n")
            
            opcion = input("Cambiar contraseña del usuario existente? (S/N): ").strip().upper()
            
            if opcion == 'S':
                print("\n--- Cambiar Contraseña ---")
                nueva_password = input("Nueva contraseña: ").strip()
                confirmar_password = input("Confirmar contraseña: ").strip()
                
                if nueva_password != confirmar_password:
                    print("\n❌ Las contraseñas no coinciden")
                    return
                
                if len(nueva_password) < 4:
                    print("\n❌ La contraseña debe tener al menos 4 caracteres")
                    return
                
                admin.set_password(nueva_password)
                db.session.commit()
                
                print("\n✅ Contraseña actualizada exitosamente")
                print(f"\n" + "="*60)
                print("CREDENCIALES PARA ACCEDER AL SISTEMA")
                print("="*60)
                print(f"  Usuario: {admin.username}")
                print(f"  Contraseña: {nueva_password}")
                print(f"  Email: {admin.email}")
                print(f"\n  URL Local: http://localhost:5001")
                print(f"  URL en Nube: https://libreria-joda.web.app")
                print("="*60)
                print("\nIMPORTANTE: Guarda estas credenciales en un lugar seguro")
                print("="*60 + "\n")
            else:
                print("\n✅ Usuario admin mantenido sin cambios")
                print(f"\nCredenciales actuales:")
                print(f"  Usuario: {admin.username}")
                print(f"  Email: {admin.email}")
        else:
            print("No se encontró usuario admin. Creando nuevo usuario...\n")
            
            username = input("Nombre de usuario (default: admin): ").strip() or 'admin'
            email = input("Email (default: admin@libreriajoda.com): ").strip() or 'admin@libreriajoda.com'
            nombre_completo = input("Nombre completo (default: Administrador): ").strip() or 'Administrador'
            
            password = getpass("Contraseña: ")
            confirmar_password = getpass("Confirmar contraseña: ")
            
            if password != confirmar_password:
                print("\n❌ Las contraseñas no coinciden")
                return
            
            if len(password) < 4:
                print("\n❌ La contraseña debe tener al menos 4 caracteres")
                return
            
            nuevo_admin = User(
                username=username,
                email=email,
                full_name=nombre_completo,
                role='admin',
                active=True
            )
            nuevo_admin.set_password(password)
            
            db.session.add(nuevo_admin)
            db.session.commit()
            
            print("\n✅ Usuario administrador creado exitosamente")
            print(f"\nCredenciales:")
            print(f"  Usuario: {username}")
            print(f"  Email: {email}")
            print(f"  Nombre: {nombre_completo}")
            print(f"\nURL una vez desplegado: https://libreria-joda.web.app")
        
        print("\n" + "="*60)
        print("IMPORTANTE: Guarda estas credenciales en un lugar seguro")
        print("="*60 + "\n")

if __name__ == '__main__':
    configurar_admin()
