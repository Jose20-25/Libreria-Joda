from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """Modelo de Usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # admin, user
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    """Modelo de Producto"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    cost_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    icon = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    sale_items = db.relationship('SaleItem', backref='product', lazy=True, cascade='all, delete-orphan')
    purchase_items = db.relationship('PurchaseItem', backref='product', lazy=True, cascade='all, delete-orphan')
    invoice_items = db.relationship('InvoiceItem', backref='product', lazy=True, cascade='all, delete-orphan')
    
    @property
    def profit_margin(self):
        if self.cost_price > 0:
            return ((self.sell_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    @property
    def status(self):
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock <= self.min_stock:
            return 'low_stock'
        return 'in_stock'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'category': self.category,
            'stock': self.stock,
            'min_stock': self.min_stock,
            'cost_price': self.cost_price,
            'sell_price': self.sell_price,
            'description': self.description,
            'location': self.location,
            'icon': self.icon,
            'status': self.status,
            'profit_margin': round(self.profit_margin, 2)
        }
    
    def __repr__(self):
        return f'<Product {self.code} - {self.name}>'

class Customer(db.Model):
    """Modelo de Cliente"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    rfc = db.Column(db.String(13))
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    customer_type = db.Column(db.String(20), default='regular')  # regular, vip
    notes = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    sales = db.relationship('Sale', backref='customer', lazy=True)
    invoices = db.relationship('Invoice', backref='customer', lazy=True)
    
    @property
    def total_purchases(self):
        return sum(sale.total for sale in self.sales)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'rfc': self.rfc,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'customer_type': self.customer_type,
            'notes': self.notes,
            'total_purchases': self.total_purchases,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }
    
    def __repr__(self):
        return f'<Customer {self.name}>'
