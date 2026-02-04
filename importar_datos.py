#!/usr/bin/env python
"""
Script para importar datos desde JSON a la base de datos
Para restaurar después de migración
"""
import json
import sys
from datetime import datetime
from app import create_app, db
from app.models.models import User, Product, Customer
from app.models.transactions import Sale, SaleItem, Purchase, PurchaseItem, Invoice, InvoiceItem

def import_data(filename):
    """Importar datos desde JSON"""
    app = create_app('production')
    
    with app.app_context():
        print(f"📥 Cargando datos desde {filename}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📅 Backup creado: {data['export_date']}")
        
        # Importar usuarios
        print("\n👤 Importando usuarios...")
        for user_data in data['users']:
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                active=user_data['active']
            )
            user.password_hash = user_data['password_hash']
            if user_data['created_at']:
                user.created_at = datetime.fromisoformat(user_data['created_at'])
            
            db.session.add(user)
        
        db.session.commit()
        print(f"   ✅ {len(data['users'])} usuarios importados")
        
        # Importar productos
        print("\n📦 Importando productos...")
        for product_data in data['products']:
            product = Product(
                id=product_data['id'],
                code=product_data['code'],
                name=product_data['name'],
                category=product_data['category'],
                stock=product_data['stock'],
                min_stock=product_data['min_stock'],
                cost_price=product_data['cost_price'],
                sell_price=product_data['sell_price'],
                description=product_data['description'],
                location=product_data['location'],
                icon=product_data['icon'],
                active=product_data['active']
            )
            if product_data['created_at']:
                product.created_at = datetime.fromisoformat(product_data['created_at'])
            
            db.session.add(product)
        
        db.session.commit()
        print(f"   ✅ {len(data['products'])} productos importados")
        
        # Importar clientes
        print("\n👥 Importando clientes...")
        for customer_data in data['customers']:
            customer = Customer(
                id=customer_data['id'],
                name=customer_data['name'],
                rfc=customer_data.get('rfc'),
                email=customer_data.get('email'),
                phone=customer_data.get('phone'),
                address=customer_data.get('address'),
                city=customer_data.get('city'),
                state=customer_data.get('state'),
                zip_code=customer_data.get('zip_code'),
                customer_type=customer_data.get('customer_type', 'regular'),
                notes=customer_data.get('notes'),
                active=customer_data.get('active', True)
            )
            if customer_data.get('created_at'):
                customer.created_at = datetime.fromisoformat(customer_data['created_at'])
            
            db.session.add(customer)
        
        db.session.commit()
        print(f"   ✅ {len(data['customers'])} clientes importados")
        
        # Importar ventas
        print("\n💰 Importando ventas...")
        for sale_data in data['sales']:
            sale = Sale(
                id=sale_data['id'],
                sale_number=sale_data['sale_number'],
                customer_id=sale_data.get('customer_id'),
                customer_name=sale_data.get('customer_name'),
                payment_method=sale_data.get('payment_method'),
                subtotal=sale_data.get('subtotal', 0),
                tax=sale_data.get('tax', 0),
                total=sale_data.get('total', 0),
                notes=sale_data.get('notes')
            )
            if sale_data.get('created_at'):
                sale.created_at = datetime.fromisoformat(sale_data['created_at'])
            
            db.session.add(sale)
            db.session.flush()
            
            for item_data in sale_data['items']:
                item = SaleItem(
                    sale_id=sale.id,
                    product_id=item_data['product_id'],
                    product_name=item_data.get('product_name'),
                    product_code=item_data.get('product_code'),
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    line_total=item_data.get('line_total', item_data['quantity'] * item_data['unit_price'])
                )
                db.session.add(item)
        
        db.session.commit()
        print(f"   ✅ {len(data['sales'])} ventas importadas")
        
        # Importar compras
        print("\n🛒 Importando compras...")
        for purchase_data in data['purchases']:
            purchase = Purchase(
                id=purchase_data['id'],
                supplier=purchase_data['supplier'],
                user_id=purchase_data['user_id'],
                total=purchase_data['total'],
                status=purchase_data['status'],
                notes=purchase_data['notes']
            )
            if purchase_data['date']:
                purchase.date = datetime.fromisoformat(purchase_data['date'])
            
            db.session.add(purchase)
            db.session.flush()
            
            for item_data in purchase_data['items']:
                item = PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
                db.session.add(item)
        
        db.session.commit()
        print(f"   ✅ {len(data['purchases'])} compras importadas")
        
        # Importar facturas
        print("\n🧾 Importando facturas...")
        for invoice_data in data['invoices']:
            invoice = Invoice(
                id=invoice_data['id'],
                invoice_number=invoice_data['invoice_number'],
                customer_id=invoice_data['customer_id'],
                customer_name=invoice_data.get('customer_name'),
                payment_method=invoice_data.get('payment_method'),
                status=invoice_data.get('status', 'pending'),
                subtotal=invoice_data.get('subtotal', 0),
                tax=invoice_data.get('tax', 0),
                total=invoice_data.get('total', 0),
                notes=invoice_data.get('notes')
            )
            if invoice_data.get('created_at'):
                invoice.created_at = datetime.fromisoformat(invoice_data['created_at'])
            
            db.session.add(invoice)
            db.session.flush()
            
            for item_data in invoice_data['items']:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=item_data['product_id'],
                    product_name=item_data.get('product_name'),
                    product_code=item_data.get('product_code'),
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    line_total=item_data.get('line_total', item_data['quantity'] * item_data['unit_price'])
                )
                db.session.add(item)
        
        db.session.commit()
        print(f"   ✅ {len(data['invoices'])} facturas importadas")
        
        print("\n🎉 ¡Importación completada exitosamente!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Uso: python importar_datos.py <archivo_backup.json>")
        sys.exit(1)
    
    import_data(sys.argv[1])
