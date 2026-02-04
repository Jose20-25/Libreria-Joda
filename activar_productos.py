#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Activar productos con stock para ventas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Product

def activar_productos_con_stock():
    """Activa todos los productos que tienen stock"""
    app = create_app()
    
    with app.app_context():
        print("🔧 ACTIVANDO PRODUCTOS CON STOCK")
        print("=" * 40)
        
        # Obtener productos con stock pero inactivos
        productos_inactivos = Product.query.filter(Product.stock > 0, Product.active == False).all()
        
        print(f"📦 Productos con stock pero inactivos: {len(productos_inactivos)}")
        
        if productos_inactivos:
            # Activar productos
            activados = 0
            for producto in productos_inactivos:
                producto.active = True
                activados += 1
                print(f"   ✅ {producto.name} - Stock: {producto.stock}")
            
            try:
                db.session.commit()
                print(f"\n✅ {activados} productos activados exitosamente")
                
                # Verificar resultado
                productos_activos = Product.query.filter_by(active=True).count()
                productos_con_stock = Product.query.filter(Product.active == True, Product.stock > 0).count()
                
                print(f"\n📊 ESTADO FINAL:")
                print(f"   🔧 Productos activos: {productos_activos}")
                print(f"   📦 Productos activos con stock: {productos_con_stock}")
                
            except Exception as e:
                db.session.rollback()
                print(f"\n❌ Error al activar productos: {e}")
        else:
            print("✅ Todos los productos con stock ya están activos")

if __name__ == "__main__":
    activar_productos_con_stock()