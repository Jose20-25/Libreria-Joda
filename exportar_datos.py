#!/usr/bin/env python
"""
Script para exportar todos los datos de SQLite a JSON
Para migrar sin perder información
"""
import json
from datetime import datetime
from app import create_app, db
from app.models.models import User, Product, Customer
from app.models.transactions import Sale, SaleItem, Purchase, PurchaseItem, Invoice, InvoiceItem

def export_data():
    """Exportar todos los datos a JSON"""
    app = create_app('development')
    
    with app.app_context():
        data = {
            'export_date': datetime.now().isoformat(),
            'users': [],
            'products': [],
            'customers': [],
            'sales': [],
            'purchases': [],
            'invoices': []
        }
        
        # Exportar usuarios
        print("📦 Exportando usuarios...")
        for user in User.query.all():
            data['users'].append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'full_name': user.full_name,
                'role': user.role,
                'active': user.active,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        # Exportar productos
        print("📦 Exportando productos...")
        for product in Product.query.all():
            data['products'].append({
                'id': product.id,
                'code': product.code,
                'name': product.name,
                'category': product.category,
                'stock': product.stock,
                'min_stock': product.min_stock,
                'cost_price': product.cost_price,
                'sell_price': product.sell_price,
                'description': product.description,
                'location': product.location,
                'icon': product.icon,
                'active': product.active,
                'created_at': product.created_at.isoformat() if product.created_at else None
            })
        
        # Exportar clientes
        print("📦 Exportando clientes...")
        for customer in Customer.query.all():
            data['customers'].append({
                'id': customer.id,
                'name': customer.name,
                'rfc': customer.rfc,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address,
                'city': customer.city,
                'state': customer.state,
                'zip_code': customer.zip_code,
                'customer_type': customer.customer_type,
                'notes': customer.notes,
                'active': customer.active,
                'created_at': customer.created_at.isoformat() if customer.created_at else None
            })
        
        # Exportar ventas
        print("📦 Exportando ventas...")
        for sale in Sale.query.all():
            sale_data = {
                'id': sale.id,
                'sale_number': sale.sale_number,
                'customer_id': sale.customer_id,
                'customer_name': sale.customer_name,
                'payment_method': sale.payment_method,
                'subtotal': sale.subtotal,
                'tax': sale.tax,
                'total': sale.total,
                'notes': sale.notes,
                'created_at': sale.created_at.isoformat() if sale.created_at else None,
                'items': []
            }
            
            for item in sale.items:
                sale_data['items'].append({
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'product_code': item.product_code,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'line_total': item.line_total
                })
            
            data['sales'].append(sale_data)
        
        # Exportar compras
        print("📦 Exportando compras...")
        for purchase in Purchase.query.all():
            purchase_data = {
                'id': purchase.id,
                'order_number': purchase.order_number,
                'supplier_name': purchase.supplier_name,
                'supplier_phone': purchase.supplier_phone,
                'order_date': purchase.order_date.isoformat() if purchase.order_date else None,
                'delivery_date': purchase.delivery_date.isoformat() if purchase.delivery_date else None,
                'status': purchase.status,
                'total': purchase.total,
                'notes': purchase.notes,
                'created_at': purchase.created_at.isoformat() if purchase.created_at else None,
                'items': []
            }
            
            for item in purchase.items:
                purchase_data['items'].append({
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'product_code': item.product_code,
                    'quantity': item.quantity,
                    'unit_cost': item.unit_cost,
                    'line_total': item.line_total
                })
            
            data['purchases'].append(purchase_data)
        
        # Exportar facturas
        print("📦 Exportando facturas...")
        for invoice in Invoice.query.all():
            invoice_data = {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'customer_id': invoice.customer_id,
                'customer_name': invoice.customer_name,
                'payment_method': invoice.payment_method,
                'status': invoice.status,
                'subtotal': invoice.subtotal,
                'tax': invoice.tax,
                'total': invoice.total,
                'notes': invoice.notes,
                'created_at': invoice.created_at.isoformat() if invoice.created_at else None,
                'items': []
            }
            
            for item in invoice.items:
                invoice_data['items'].append({
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'product_code': item.product_code,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'line_total': item.line_total
                })
            
            data['invoices'].append(invoice_data)
        
        # Guardar a archivo JSON
        filename = f'datos_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Datos exportados exitosamente a: {filename}")
        print(f"   - Usuarios: {len(data['users'])}")
        print(f"   - Productos: {len(data['products'])}")
        print(f"   - Clientes: {len(data['customers'])}")
        print(f"   - Ventas: {len(data['sales'])}")
        print(f"   - Compras: {len(data['purchases'])}")
        print(f"   - Facturas: {len(data['invoices'])}")
        
        return filename

if __name__ == '__main__':
    export_data()
