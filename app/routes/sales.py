from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.models import Product, Customer
from app.models.transactions import Sale, SaleItem, Invoice, InvoiceItem
from datetime import datetime

bp = Blueprint('sales', __name__, url_prefix='/sales')

@bp.route('/')
@login_required
def index():
    """Página principal de ventas (POS)"""
    products = Product.query.filter_by(active=True).filter(Product.stock > 0).all()
    customers = Customer.query.filter_by(active=True).all()
    
    # Obtener las últimas 10 ventas
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(10).all()
    
    return render_template('sales/index.html', 
                         products=products,
                         customers=customers,
                         recent_sales=recent_sales)

@bp.route('/api/sales')
@login_required
def get_sales():
    """API: Obtener todas las ventas"""
    sales = Sale.query.order_by(Sale.created_at.desc()).all()
    return jsonify([s.to_dict() for s in sales])

@bp.route('/api/sales/<int:sale_id>')
@login_required
def get_sale(sale_id):
    """API: Obtener una venta específica"""
    sale = Sale.query.get_or_404(sale_id)
    return jsonify(sale.to_dict())

@bp.route('/api/sales', methods=['POST'])
@login_required
def create_sale():
    """API: Crear nueva venta"""
    data = request.get_json()
    
    # Crear venta
    sale = Sale(
        sale_number=f"V-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        customer_id=data.get('customer_id'),
        customer_name=data.get('customer_name', 'Público General'),
        payment_method=data['payment_method']
    )
    
    db.session.add(sale)
    db.session.flush()  # Para obtener el ID de la venta
    
    # Agregar items
    for item_data in data['items']:
        product = Product.query.get(item_data['product_id'])
        
        # Verificar stock
        if product.stock < item_data['quantity']:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Stock insuficiente para {product.name}'
            }), 400
        
        # Crear item
        item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            product_name=product.name,
            product_code=product.code,
            quantity=item_data['quantity'],
            unit_price=product.sell_price
        )
        item.calculate_line_total()
        db.session.add(item)
        
        # Actualizar stock
        product.stock -= item_data['quantity']
    
    # Crear factura automáticamente
    invoice = Invoice(
        invoice_number=f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        customer_id=data.get('customer_id') or 1,  # Usar ID 1 como default si no se especifica
        customer_name=data.get('customer_name', 'Público General'),
        payment_method=data['payment_method'],
        status='paid',  # La venta ya está pagada
        notes=f"Generada automáticamente desde venta {sale.sale_number}"
    )
    
    db.session.add(invoice)
    db.session.flush()  # Para obtener el ID de la factura
    
    # Duplicar items en la factura
    for sale_item in sale.items:
        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=sale_item.product_id,
            product_name=sale_item.product_name,
            product_code=sale_item.product_code,
            quantity=sale_item.quantity,
            unit_price=sale_item.unit_price
        )
        invoice_item.calculate_line_total()
        db.session.add(invoice_item)
    
    # Calcular totales para venta y factura
    sale.calculate_totals()
    invoice.calculate_totals()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Venta procesada y factura {invoice.invoice_number} generada automáticamente',
        'sale': sale.to_dict(),
        'invoice': invoice.to_dict()
    }), 201
