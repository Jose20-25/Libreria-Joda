from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.models import Product
from app.models.transactions import Purchase, PurchaseItem
from datetime import datetime

bp = Blueprint('purchases', __name__, url_prefix='/purchases')

@bp.route('/')
@login_required
def index():
    """Página principal de compras"""
    purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()
    products = Product.query.filter_by(active=True).all()
    return render_template('purchases/index.html', 
                         purchases=purchases,
                         products=products)

@bp.route('/api/purchases')
@login_required
def get_purchases():
    """API: Obtener todas las compras"""
    purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()
    return jsonify([p.to_dict() for p in purchases])

@bp.route('/api/purchases/<int:purchase_id>')
@login_required
def get_purchase(purchase_id):
    """API: Obtener una compra específica"""
    purchase = Purchase.query.get_or_404(purchase_id)
    return jsonify(purchase.to_dict())

@bp.route('/api/purchases', methods=['POST'])
@login_required
def create_purchase():
    """API: Crear nueva orden de compra"""
    data = request.get_json()
    
    # Crear compra
    purchase = Purchase(
        order_number=f"OC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        supplier_name=data['supplier_name'],
        supplier_phone=data.get('supplier_phone', ''),
        delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d') if data.get('delivery_date') else None,
        notes=data.get('notes', '')
    )
    
    db.session.add(purchase)
    db.session.flush()
    
    # Agregar items
    for item_data in data['items']:
        product = Product.query.get(item_data['product_id'])
        
        item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=product.id,
            product_name=product.name,
            product_code=product.code,
            quantity=item_data['quantity'],
            unit_cost=item_data['unit_cost']
        )
        item.calculate_line_total()
        db.session.add(item)
    
    # Calcular total
    purchase.calculate_total()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Orden de compra creada exitosamente',
        'purchase': purchase.to_dict()
    }), 201

@bp.route('/api/purchases/<int:purchase_id>/receive', methods=['POST'])
@login_required
def receive_purchase(purchase_id):
    """API: Recibir orden de compra y actualizar inventario"""
    purchase = Purchase.query.get_or_404(purchase_id)
    
    if purchase.status == 'received':
        return jsonify({
            'success': False,
            'message': 'Esta orden ya fue recibida'
        }), 400
    
    # Actualizar stock de productos
    for item in purchase.items:
        product = Product.query.get(item.product_id)
        product.stock += item.quantity
        product.cost_price = item.unit_cost  # Actualizar precio de costo
    
    purchase.status = 'received'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Orden recibida e inventario actualizado'
    })
