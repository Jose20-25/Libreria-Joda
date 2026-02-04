#!/bin/bash
# Script de inicialización para Render.com

echo "Inicializando base de datos..."

# Crear directorio instance si no existe
mkdir -p instance

# Ejecutar migraciones o crear tablas
python << END
from app import create_app, db
from app.models.models import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()
    
    # Verificar si existe el usuario admin
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        # Crear usuario admin por defecto
        admin = User(
            username='admin',
            email='admin@libreriajoda.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Usuario admin creado exitosamente")
    else:
        print("Usuario admin ya existe")
    
    print("Base de datos inicializada correctamente")

END

echo "Inicialización completada"
