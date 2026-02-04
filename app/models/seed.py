from app import db
from app.models.models import User, Product, Customer
from app.models.transactions import Sale, SaleItem, Purchase, PurchaseItem, Invoice, InvoiceItem, SystemConfig
from datetime import datetime, timedelta

def create_sample_data():
    """Crea datos de ejemplo para el sistema"""
    
    # Verificar si ya existen datos
    if User.query.first() is not None:
        return
    
    # Crear usuario administrador
    admin = User(
        username='admin',
        email='admin@libreriajoda.com',
        full_name='Administrador JODA',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Crear configuración del sistema
    config = SystemConfig(
        company_name='LIBRERÍA JODA',
        company_rfc='JODA123456ABC',
        company_phone='55-1234-5678',
        company_email='contacto@libreriajoda.com',
        company_address='Av. Principal 123',
        company_city='Ciudad de México',
        company_state='CDMX'
    )
    db.session.add(config)
    
    # Crear productos de ejemplo
    products_data = [
        {'code': 'CUA-001', 'name': 'Cuaderno Profesional 100 hojas', 'category': 'Cuadernos', 'stock': 50, 'min_stock': 10, 'cost_price': 15.00, 'sell_price': 25.00, 'icon': 'book', 'location': 'A-1'},
        {'code': 'LAP-001', 'name': 'Lápiz del #2 Mirado', 'category': 'Lápices', 'stock': 120, 'min_stock': 20, 'cost_price': 3.00, 'sell_price': 5.00, 'icon': 'pencil-alt', 'location': 'B-1'},
        {'code': 'BOL-001', 'name': 'Bolígrafo Bic Negro', 'category': 'Bolígrafos', 'stock': 80, 'min_stock': 15, 'cost_price': 4.00, 'sell_price': 7.00, 'icon': 'pen', 'location': 'B-2'},
        {'code': 'MAR-001', 'name': 'Marcador Permanente Sharpie', 'category': 'Marcadores', 'stock': 45, 'min_stock': 10, 'cost_price': 18.00, 'sell_price': 30.00, 'icon': 'marker', 'location': 'C-1'},
        {'code': 'COL-001', 'name': 'Colores Prismacolor 24 piezas', 'category': 'Colores', 'stock': 25, 'min_stock': 5, 'cost_price': 150.00, 'sell_price': 250.00, 'icon': 'palette', 'location': 'C-2'},
        {'code': 'TIJ-001', 'name': 'Tijeras Escolares Punta Roma', 'category': 'Tijeras', 'stock': 30, 'min_stock': 10, 'cost_price': 20.00, 'sell_price': 35.00, 'icon': 'cut', 'location': 'D-1'},
        {'code': 'CAL-001', 'name': 'Calculadora Científica Casio', 'category': 'Calculadoras', 'stock': 15, 'min_stock': 5, 'cost_price': 250.00, 'sell_price': 400.00, 'icon': 'calculator', 'location': 'E-1'},
        {'code': 'MOC-001', 'name': 'Mochila Escolar Grande', 'category': 'Mochilas', 'stock': 8, 'min_stock': 3, 'cost_price': 300.00, 'sell_price': 500.00, 'icon': 'shopping-bag', 'location': 'F-1'},
    ]
    
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    
    # Crear clientes de ejemplo
    customers_data = [
        {'name': 'María González López', 'email': 'maria.gonzalez@email.com', 'phone': '55-9876-5432', 'rfc': 'GOLM850315ABC', 'customer_type': 'vip', 'city': 'Ciudad de México', 'state': 'CDMX'},
        {'name': 'Carlos Rodríguez Pérez', 'email': 'carlos.rodriguez@email.com', 'phone': '55-1234-9876', 'rfc': 'ROPC900520DEF', 'customer_type': 'regular', 'city': 'Monterrey', 'state': 'Nuevo León'},
        {'name': 'Ana Martínez Sánchez', 'email': 'ana.martinez@email.com', 'phone': '55-5555-1234', 'customer_type': 'regular', 'city': 'Guadalajara', 'state': 'Jalisco'},
    ]
    
    for customer_data in customers_data:
        customer = Customer(**customer_data)
        db.session.add(customer)
    
    # Commit inicial para obtener los IDs
    db.session.commit()
    
    # Crear venta de ejemplo
    sale = Sale(
        sale_number=f'V-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        customer_id=1,
        customer_name='María González López',
        payment_method='card'
    )
    db.session.add(sale)
    db.session.commit()
    
    # Añadir items a la venta
    product1 = Product.query.filter_by(code='CUA-001').first()
    product2 = Product.query.filter_by(code='LAP-001').first()
    
    item1 = SaleItem(
        sale_id=sale.id,
        product_id=product1.id,
        product_name=product1.name,
        product_code=product1.code,
        quantity=3,
        unit_price=product1.sell_price
    )
    item1.calculate_line_total()
    db.session.add(item1)
    
    item2 = SaleItem(
        sale_id=sale.id,
        product_id=product2.id,
        product_name=product2.name,
        product_code=product2.code,
        quantity=5,
        unit_price=product2.sell_price
    )
    item2.calculate_line_total()
    db.session.add(item2)
    
    # Actualizar stock
    product1.stock -= 3
    product2.stock -= 5
    
    # Calcular totales de venta
    sale.calculate_totals()
    
    db.session.commit()
    
    print("✅ Datos de ejemplo creados exitosamente")
