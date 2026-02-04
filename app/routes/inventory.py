from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.models import Product
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

CATEGORIES = [
    'Cuadernos', 'Lápices', 'Bolígrafos', 'Marcadores', 'Colores', 
    'Tijeras', 'Correctores', 'Reglas', 'Folders', 'Mochilas', 
    'Calculadoras', 'Papel', 'Arte', 'Accesorios'
]

CATEGORY_PREFIXES = {
    'Cuadernos': 'CUA', 'Lápices': 'LAP', 'Bolígrafos': 'BOL',
    'Marcadores': 'MAR', 'Colores': 'COL', 'Tijeras': 'TIJ',
    'Correctores': 'COR', 'Reglas': 'REG', 'Folders': 'FOL',
    'Mochilas': 'MOC', 'Calculadoras': 'CAL', 'Papel': 'PAP',
    'Arte': 'ART', 'Accesorios': 'ACC'
}

@bp.route('/')
@login_required
def index():
    """Página principal de inventario"""
    products = Product.query.filter_by(active=True).all()
    return render_template('inventory/index.html', 
                         products=products,
                         categories=CATEGORIES)

@bp.route('/api/products')
@login_required
def get_products():
    """API: Obtener todos los productos"""
    status = request.args.get('status', 'all')
    category = request.args.get('category')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(active=True)
    
    # Filtrar por categoría
    if category:
        query = query.filter_by(category=category)
    
    # Filtrar por búsqueda
    if search:
        query = query.filter(
            (Product.name.contains(search)) | 
            (Product.code.contains(search))
        )
    
    products = query.all()
    
    # Filtrar por estado de stock
    if status != 'all':
        products = [p for p in products if p.status == status]
    
    return jsonify([p.to_dict() for p in products])

@bp.route('/api/products/<int:product_id>')
@login_required
def get_product(product_id):
    """API: Obtener un producto específico"""
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'success': True,
        'data': product.to_dict()
    })

@bp.route('/api/products', methods=['POST'])
@login_required
def create_product():
    """API: Crear nuevo producto"""
    data = request.get_json()
    
    # Generar código si no existe
    if not data.get('code'):
        category = data.get('category')
        prefix = CATEGORY_PREFIXES.get(category, 'PROD')
        
        # Obtener el último número de la categoría
        last_product = Product.query.filter(
            Product.code.startswith(prefix)
        ).order_by(Product.code.desc()).first()
        
        if last_product:
            try:
                last_num = int(last_product.code.split('-')[1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        data['code'] = f"{prefix}-{new_num:03d}"
    
    # Crear producto
    product = Product(
        code=data['code'],
        name=data['name'],
        category=data['category'],
        stock=data.get('stock', 0),
        min_stock=data.get('min_stock', 10),
        cost_price=data['cost_price'],
        sell_price=data['sell_price'],
        description=data.get('description', ''),
        location=data.get('location', ''),
        icon=data.get('icon', 'box')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto creado exitosamente',
        'product': product.to_dict()
    }), 201

@bp.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """API: Actualizar producto"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Actualizar campos
    product.name = data.get('name', product.name)
    product.category = data.get('category', product.category)
    product.stock = data.get('stock', product.stock)
    product.min_stock = data.get('min_stock', product.min_stock)
    product.cost_price = data.get('cost_price', product.cost_price)
    product.sell_price = data.get('sell_price', product.sell_price)
    product.description = data.get('description', product.description)
    product.location = data.get('location', product.location)
    product.icon = data.get('icon', product.icon)
    product.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto actualizado exitosamente',
        'product': product.to_dict()
    })

@bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """API: Eliminar producto (soft delete)"""
    product = Product.query.get_or_404(product_id)
    product.active = False
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Producto eliminado exitosamente'
    })

@bp.route('/api/generate-code')
@login_required
def generate_code():
    """API: Generar código automático para una categoría"""
    category = request.args.get('category')
    prefix = CATEGORY_PREFIXES.get(category, 'PROD')
    
    # Obtener el último número de la categoría
    last_product = Product.query.filter(
        Product.code.startswith(prefix)
    ).order_by(Product.code.desc()).first()
    
    if last_product:
        try:
            last_num = int(last_product.code.split('-')[1])
            new_num = last_num + 1
        except:
            new_num = 1
    else:
        new_num = 1
    
    code = f"{prefix}-{new_num:03d}"
    
    return jsonify({'code': code})
