from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.models import Customer
from app.models.transactions import Sale

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/')
@login_required
def index():
    """Página principal de clientes"""
    customers = Customer.query.filter_by(active=True).all()
    return render_template('customers/index.html', customers=customers)

@bp.route('/api/customers')
@login_required
def get_customers():
    """API: Obtener todos los clientes"""
    customers = Customer.query.filter_by(active=True).all()
    return jsonify([c.to_dict() for c in customers])

@bp.route('/api/customers/<int:customer_id>')
@login_required
def get_customer(customer_id):
    """API: Obtener un cliente específico"""
    customer = Customer.query.get_or_404(customer_id)
    
    # Obtener historial de compras
    purchases = Sale.query.filter_by(customer_id=customer_id).order_by(Sale.created_at.desc()).all()
    
    data = customer.to_dict()
    data['purchases'] = [p.to_dict() for p in purchases]
    
    return jsonify(data)

@bp.route('/api/customers', methods=['POST'])
@login_required
def create_customer():
    """API: Crear nuevo cliente"""
    data = request.get_json()
    
    customer = Customer(
        name=data['name'],
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        rfc=data.get('rfc', ''),
        address=data.get('address', ''),
        city=data.get('city', ''),
        state=data.get('state', ''),
        zip_code=data.get('zip_code', ''),
        customer_type=data.get('customer_type', 'regular'),
        notes=data.get('notes', '')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cliente creado exitosamente',
        'customer': customer.to_dict()
    }), 201

@bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    """API: Actualizar cliente"""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.rfc = data.get('rfc', customer.rfc)
    customer.address = data.get('address', customer.address)
    customer.city = data.get('city', customer.city)
    customer.state = data.get('state', customer.state)
    customer.zip_code = data.get('zip_code', customer.zip_code)
    customer.customer_type = data.get('customer_type', customer.customer_type)
    customer.notes = data.get('notes', customer.notes)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cliente actualizado exitosamente',
        'customer': customer.to_dict()
    })

@bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    """API: Eliminar cliente (soft delete)"""
    customer = Customer.query.get_or_404(customer_id)
    customer.active = False
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cliente eliminado exitosamente'
    })
