#!/usr/bin/env python
"""
LIBRERÍA JODA - Sistema ERP
Punto de entrada principal de la aplicación
"""
import os
from app import create_app, db, login_manager
from app.models import User

# Crear aplicación
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Configurar login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Comandos CLI
@app.cli.command()
def init_db():
    """Inicializar la base de datos"""
    db.create_all()
    print('✅ Base de datos inicializada')

@app.cli.command()
def seed_db():
    """Llenar la base de datos con datos de prueba"""
    from app.models.seed import create_sample_data
    create_sample_data()
    print('✅ Datos de prueba creados')

@app.cli.command()
def create_admin():
    """Crear usuario administrador"""
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')
    full_name = input('Full Name: ')
    
    user = User(username=username, email=email, full_name=full_name, role='admin')
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print(f'✅ Usuario administrador {username} creado exitosamente')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
