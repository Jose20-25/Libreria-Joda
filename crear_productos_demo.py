#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar productos de ejemplo
Sistema de Librería JODA - Demostración del reporte profesional
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Product
from datetime import datetime
import random

def crear_productos_ejemplo():
    """Crea productos de ejemplo para demostrar el reporte"""
    app = create_app()
    
    productos_ejemplo = [
        # Cuadernos
        {"code": "CUA001", "name": "Cuaderno Universitario 100 Hojas", "category": "Cuadernos", "stock": 5, "min_stock": 15, "cost_price": 8.50, "sell_price": 12.00},
        {"code": "CUA002", "name": "Cuaderno Escolar Rayado", "category": "Cuadernos", "stock": 25, "min_stock": 20, "cost_price": 4.00, "sell_price": 6.50},
        {"code": "CUA003", "name": "Cuaderno Profesional Pasta Dura", "category": "Cuadernos", "stock": 0, "min_stock": 10, "cost_price": 15.00, "sell_price": 22.00},
        
        # Lápices
        {"code": "LAP001", "name": "Lápiz HB Mirado Classic", "category": "Lápices", "stock": 50, "min_stock": 30, "cost_price": 1.20, "sell_price": 2.50},
        {"code": "LAP002", "name": "Lápiz 2B Dibujo Técnico", "category": "Lápices", "stock": 8, "min_stock": 15, "cost_price": 2.80, "sell_price": 4.50},
        {"code": "LAP003", "name": "Lápiz Mecánico 0.5mm", "category": "Lápices", "stock": 15, "min_stock": 12, "cost_price": 12.00, "sell_price": 18.00},
        
        # Bolígrafos
        {"code": "BOL001", "name": "Bolígrafo BIC Azul", "category": "Bolígrafos", "stock": 45, "min_stock": 25, "cost_price": 0.80, "sell_price": 1.50},
        {"code": "BOL002", "name": "Bolígrafo Pilot G2 Negro", "category": "Bolígrafos", "stock": 3, "min_stock": 20, "cost_price": 5.50, "sell_price": 9.00},
        {"code": "BOL003", "name": "Bolígrafo Gel Multicolor Set", "category": "Bolígrafos", "stock": 12, "min_stock": 8, "cost_price": 25.00, "sell_price": 38.00},
        
        # Marcadores
        {"code": "MAR001", "name": "Marcador Sharpie Negro", "category": "Marcadores", "stock": 18, "min_stock": 15, "cost_price": 8.00, "sell_price": 12.50},
        {"code": "MAR002", "name": "Marcadores Fluorescentes Set 6", "category": "Marcadores", "stock": 2, "min_stock": 10, "cost_price": 15.00, "sell_price": 24.00},
        {"code": "MAR003", "name": "Marcador para Pizarrón", "category": "Marcadores", "stock": 0, "min_stock": 12, "cost_price": 6.50, "sell_price": 11.00},
        
        # Colores
        {"code": "COL001", "name": "Colores Prismacolor Set 24", "category": "Colores", "stock": 8, "min_stock": 6, "cost_price": 45.00, "sell_price": 68.00},
        {"code": "COL002", "name": "Crayolas Caja 64 Colores", "category": "Colores", "stock": 14, "min_stock": 10, "cost_price": 18.00, "sell_price": 28.00},
        {"code": "COL003", "name": "Acuarelas Profesionales", "category": "Colores", "stock": 1, "min_stock": 8, "cost_price": 35.00, "sell_price": 55.00},
        
        # Tijeras
        {"code": "TIJ001", "name": "Tijeras Escolares Punta Roma", "category": "Tijeras", "stock": 22, "min_stock": 15, "cost_price": 3.50, "sell_price": 6.00},
        {"code": "TIJ002", "name": "Tijeras Profesionales", "category": "Tijeras", "stock": 6, "min_stock": 8, "cost_price": 12.00, "sell_price": 19.00},
        
        # Correctores
        {"code": "COR001", "name": "Corrector Líquido BIC", "category": "Correctores", "stock": 28, "min_stock": 20, "cost_price": 2.50, "sell_price": 4.50},
        {"code": "COR002", "name": "Corrector Cinta", "category": "Correctores", "stock": 4, "min_stock": 15, "cost_price": 8.00, "sell_price": 13.00},
        
        # Reglas
        {"code": "REG001", "name": "Regla 30cm Transparente", "category": "Reglas", "stock": 35, "min_stock": 25, "cost_price": 1.50, "sell_price": 3.00},
        {"code": "REG002", "name": "Juego Geométrico", "category": "Reglas", "stock": 9, "min_stock": 12, "cost_price": 15.00, "sell_price": 25.00},
        
        # Folders
        {"code": "FOL001", "name": "Folder Tamaño Carta", "category": "Folders", "stock": 0, "min_stock": 30, "cost_price": 0.75, "sell_price": 1.50},
        {"code": "FOL002", "name": "Carpeta Argollada", "category": "Folders", "stock": 18, "min_stock": 15, "cost_price": 8.50, "sell_price": 14.00},
        
        # Mochilas
        {"code": "MOC001", "name": "Mochila Escolar Básica", "category": "Mochilas", "stock": 7, "min_stock": 5, "cost_price": 85.00, "sell_price": 120.00},
        {"code": "MOC002", "name": "Mochila Universitaria", "category": "Mochilas", "stock": 3, "min_stock": 8, "cost_price": 150.00, "sell_price": 220.00},
        
        # Calculadoras
        {"code": "CAL001", "name": "Calculadora Básica", "category": "Calculadoras", "stock": 12, "min_stock": 8, "cost_price": 25.00, "sell_price": 40.00},
        {"code": "CAL002", "name": "Calculadora Científica", "category": "Calculadoras", "stock": 0, "min_stock": 6, "cost_price": 180.00, "sell_price": 280.00},
        
        # Papel
        {"code": "PAP001", "name": "Papel Bond Tamaño Carta", "category": "Papel", "stock": 45, "min_stock": 20, "cost_price": 35.00, "sell_price": 50.00},
        {"code": "PAP002", "name": "Papel Construcción Colores", "category": "Papel", "stock": 8, "min_stock": 15, "cost_price": 12.00, "sell_price": 20.00},
        
        # Arte
        {"code": "ART001", "name": "Pincel Set Profesional", "category": "Arte", "stock": 6, "min_stock": 4, "cost_price": 65.00, "sell_price": 95.00},
        {"code": "ART002", "name": "Lienzo para Pintura 20x30", "category": "Arte", "stock": 2, "min_stock": 10, "cost_price": 22.00, "sell_price": 35.00},
        
        # Accesorios
        {"code": "ACC001", "name": "Grapadora Pequeña", "category": "Accesorios", "stock": 15, "min_stock": 8, "cost_price": 18.00, "sell_price": 28.00},
        {"code": "ACC002", "name": "Perforadora de Papel", "category": "Accesorios", "stock": 1, "min_stock": 6, "cost_price": 45.00, "sell_price": 70.00},
        {"code": "ACC003", "name": "Pegamento en Barra", "category": "Accesorios", "stock": 32, "min_stock": 25, "cost_price": 2.80, "sell_price": 5.00},
    ]
    
    with app.app_context():
        productos_creados = 0
        productos_actualizados = 0
        
        for producto_data in productos_ejemplo:
            # Verificar si ya existe
            existing = Product.query.filter_by(code=producto_data['code']).first()
            
            if existing:
                # Actualizar stock si es diferente
                if existing.stock != producto_data['stock']:
                    existing.stock = producto_data['stock']
                    existing.min_stock = producto_data['min_stock']
                    productos_actualizados += 1
            else:
                # Crear nuevo producto
                producto = Product(
                    code=producto_data['code'],
                    name=producto_data['name'],
                    category=producto_data['category'],
                    stock=producto_data['stock'],
                    min_stock=producto_data['min_stock'],
                    cost_price=producto_data['cost_price'],
                    sell_price=producto_data['sell_price'],
                    description=f"Producto de categoría {producto_data['category']}",
                    active=True
                )
                
                db.session.add(producto)
                productos_creados += 1
        
        try:
            db.session.commit()
            print(f"✅ Productos creados: {productos_creados}")
            print(f"✅ Productos actualizados: {productos_actualizados}")
            print(f"📊 Total productos en catálogo: {productos_creados + productos_actualizados}")
            
            # Estadísticas de stock
            productos_stock_bajo = len([p for p in productos_ejemplo if p['stock'] <= p['min_stock'] and p['stock'] > 0])
            productos_sin_stock = len([p for p in productos_ejemplo if p['stock'] == 0])
            
            print(f"⚠️ Productos con stock bajo: {productos_stock_bajo}")
            print(f"🔴 Productos sin stock: {productos_sin_stock}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear productos: {e}")
            db.session.rollback()
            return False

def main():
    """Función principal"""
    print("🏪 CREANDO PRODUCTOS DE EJEMPLO PARA REPORTE PROFESIONAL")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if crear_productos_ejemplo():
        print()
        print("🎉 ¡PRODUCTOS CREADOS EXITOSAMENTE!")
        print()
        print("📋 Ahora puedes probar el reporte profesional:")
        print("   1. Ve a: http://127.0.0.1:5001/reports")
        print("   2. Haz clic en 'Excel Inventario Pro'")
        print("   3. ¡Disfruta del reporte profesional con:")
        print("      ✅ Gráficos interactivos")
        print("      ✅ Categorías con colores")
        print("      ✅ Productos con stock bajo resaltados")
        print("      ✅ Múltiples hojas especializadas")
        print("      ✅ Análisis estadístico completo")
    else:
        print("❌ Error al crear productos")

if __name__ == "__main__":
    main()