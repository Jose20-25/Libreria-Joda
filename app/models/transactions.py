from datetime import datetime
from app import db

class Sale(db.Model):
    """Modelo de Venta"""
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer_name = db.Column(db.String(200))
    payment_method = db.Column(db.String(50))  # cash, card
    subtotal = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calcula solo el total de venta sin IVA"""
        self.total = sum(item.line_total for item in self.items)
        # Sin IVA - el precio es el total final
        self.subtotal = self.total  # Mismo valor que total
        self.tax = 0  # Sin impuestos
    
    def to_dict(self):
        return {
            'id': self.id,
            'sale_number': self.sale_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'payment_method': self.payment_method,
            'subtotal': round(self.subtotal, 2),
            'tax': round(self.tax, 2),
            'total': round(self.total, 2),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Sale {self.sale_number}>'

class SaleItem(db.Model):
    """Modelo de Item de Venta"""
    __tablename__ = 'sale_items'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))
    product_code = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    
    def calculate_line_total(self):
        """Calcula el total de la línea"""
        self.line_total = self.quantity * self.unit_price
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_code': self.product_code,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'line_total': round(self.line_total, 2)
        }
    
    def __repr__(self):
        return f'<SaleItem {self.product_name} x{self.quantity}>'

class Purchase(db.Model):
    """Modelo de Compra"""
    __tablename__ = 'purchases'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    supplier_name = db.Column(db.String(200), nullable=False)
    supplier_phone = db.Column(db.String(20))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, received, cancelled, partial
    total = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('PurchaseItem', backref='purchase', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        """Calcula el total de la compra"""
        self.total = sum(item.line_total for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'supplier_name': self.supplier_name,
            'supplier_phone': self.supplier_phone,
            'order_date': self.order_date.strftime('%Y-%m-%d'),
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d') if self.delivery_date else None,
            'status': self.status,
            'total': round(self.total, 2),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Purchase {self.order_number}>'

class PurchaseItem(db.Model):
    """Modelo de Item de Compra"""
    __tablename__ = 'purchase_items'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))
    product_code = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    
    def calculate_line_total(self):
        """Calcula el total de la línea"""
        self.line_total = self.quantity * self.unit_cost
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_code': self.product_code,
            'quantity': self.quantity,
            'unit_cost': round(self.unit_cost, 2),
            'line_total': round(self.line_total, 2)
        }
    
    def __repr__(self):
        return f'<PurchaseItem {self.product_name} x{self.quantity}>'

class Invoice(db.Model):
    """Modelo de Factura"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer_name = db.Column(db.String(200))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # paid, pending, cancelled
    subtotal = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calcula solo el total de venta sin IVA"""
        self.total = sum(item.line_total for item in self.items)
        # Sin IVA - el precio es el total final
        self.subtotal = self.total  # Mismo valor que total
        self.tax = 0  # Sin impuestos
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'payment_method': self.payment_method,
            'status': self.status,
            'subtotal': round(self.subtotal, 2),
            'tax': round(self.tax, 2),
            'total': round(self.total, 2),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'

class InvoiceItem(db.Model):
    """Modelo de Item de Factura"""
    __tablename__ = 'invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))
    product_code = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    
    def calculate_line_total(self):
        """Calcula el total de la línea"""
        self.line_total = self.quantity * self.unit_price
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_code': self.product_code,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'line_total': round(self.line_total, 2)
        }
    
    def __repr__(self):
        return f'<InvoiceItem {self.product_name} x{self.quantity}>'

class SystemConfig(db.Model):
    """Modelo de Configuración del Sistema"""
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='LIBRERÍA JODA')
    company_rfc = db.Column(db.String(13))
    company_phone = db.Column(db.String(20))
    company_email = db.Column(db.String(120))
    company_address = db.Column(db.String(300))
    company_city = db.Column(db.String(100))
    company_state = db.Column(db.String(100))
    tax_rate = db.Column(db.Float, default=16.0)
    currency = db.Column(db.String(3), default='MXN')
    low_stock_notification = db.Column(db.Boolean, default=True)
    auto_save = db.Column(db.Boolean, default=True)
    delete_confirmation = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_rfc': self.company_rfc,
            'company_phone': self.company_phone,
            'company_email': self.company_email,
            'company_address': self.company_address,
            'company_city': self.company_city,
            'company_state': self.company_state,
            'tax_rate': self.tax_rate,
            'currency': self.currency,
            'low_stock_notification': self.low_stock_notification,
            'auto_save': self.auto_save,
            'delete_confirmation': self.delete_confirmation
        }
    
    def __repr__(self):
        return f'<SystemConfig {self.company_name}>'
