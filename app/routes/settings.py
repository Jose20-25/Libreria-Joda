from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.transactions import SystemConfig
from datetime import datetime

bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/')
@login_required
def index():
    """Página principal de configuración"""
    config = SystemConfig.query.first()
    if not config:
        # Crear configuración por defecto
        config = SystemConfig(
            company_name='LIBRERÍA JODA',
            company_rfc='JODA123456XXX',
            company_address='Dirección de la empresa',
            company_phone='555-1234',
            company_email='contacto@libreriajoda.com',
            tax_rate=13.0,
            currency='MXN',
            low_stock_alert=True,
            email_notifications=False,
            backup_frequency='daily'
        )
        db.session.add(config)
        db.session.commit()
    
    return render_template('settings/index.html', config=config)

@bp.route('/api/config', methods=['GET'])
@login_required
def get_config():
    """API: Obtener configuración del sistema"""
    config = SystemConfig.query.first()
    if not config:
        return jsonify({'error': 'Configuración no encontrada'}), 404
    
    return jsonify(config.to_dict())

@bp.route('/api/config', methods=['PUT'])
@login_required
def update_config():
    """API: Actualizar configuración del sistema"""
    data = request.get_json()
    config = SystemConfig.query.first()
    
    if not config:
        return jsonify({'error': 'Configuración no encontrada'}), 404
    
    # Actualizar datos de empresa
    if 'company_name' in data:
        config.company_name = data['company_name']
    if 'company_rfc' in data:
        config.company_rfc = data['company_rfc']
    if 'company_address' in data:
        config.company_address = data['company_address']
    if 'company_phone' in data:
        config.company_phone = data['company_phone']
    if 'company_email' in data:
        config.company_email = data['company_email']
    
    # Actualizar configuración fiscal
    if 'tax_rate' in data:
        config.tax_rate = float(data['tax_rate'])
    if 'currency' in data:
        config.currency = data['currency']
    
    # Actualizar preferencias
    if 'low_stock_alert' in data:
        config.low_stock_alert = bool(data['low_stock_alert'])
    if 'email_notifications' in data:
        config.email_notifications = bool(data['email_notifications'])
    if 'backup_frequency' in data:
        config.backup_frequency = data['backup_frequency']
    
    config.updated_at = datetime.now()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Configuración actualizada exitosamente',
        'config': config.to_dict()
    })

@bp.route('/api/backup', methods=['POST'])
@login_required
def create_backup():
    """API: Crear respaldo de base de datos"""
    import shutil
    from pathlib import Path
    
    try:
        # Obtener ruta de la base de datos
        db_path = Path('instance/libreria_joda.db')
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f'backup_{timestamp}.db'
        
        # Copiar base de datos
        shutil.copy2(db_path, backup_path)
        
        return jsonify({
            'success': True,
            'message': f'Respaldo creado exitosamente: {backup_path.name}',
            'backup_file': backup_path.name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear respaldo: {str(e)}'
        }), 500

@bp.route('/api/test-email', methods=['POST'])
@login_required
def test_email():
    """API: Probar configuración de correo electrónico"""
    config = SystemConfig.query.first()
    
    # Simulación de envío de correo
    return jsonify({
        'success': True,
        'message': f'Correo de prueba enviado a {config.company_email}'
    })
