from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Función factory para crear la aplicación Flask"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    
    # Registrar blueprints
    from app.routes import inventory, sales, purchases, customers, invoices, reports, settings, main, auth
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(purchases.bp)
    app.register_blueprint(customers.bp)
    app.register_blueprint(invoices.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(settings.bp)
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
        # Crear datos de ejemplo
        from app.models.seed import create_sample_data
        create_sample_data()
    
    return app
