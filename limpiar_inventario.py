#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar productos de ejemplo del inventario
Sistema de Librería JODA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Product
from datetime import datetime

def limpiar_productos_ejemplo():
    """Elimina los productos de ejemplo que agregué anteriormente"""
    app = create_app()
    
    # Códigos de productos de ejemplo que agregué
    codigos_ejemplo = [
        'CUA001', 'CUA002', 'CUA003',  # Cuadernos
        'LAP001', 'LAP002', 'LAP003',  # Lápices
        'BOL001', 'BOL002', 'BOL003',  # Bolígrafos
        'MAR001', 'MAR002', 'MAR003',  # Marcadores
        'COL001', 'COL002', 'COL003',  # Colores
        'TIJ001', 'TIJ002',            # Tijeras
        'COR001', 'COR002',            # Correctores
        'REG001', 'REG002',            # Reglas
        'FOL001', 'FOL002',            # Folders
        'MOC001', 'MOC002',            # Mochilas
        'CAL001', 'CAL002',            # Calculadoras
        'PAP001', 'PAP002',            # Papel
        'ART001', 'ART002',            # Arte
        'ACC001', 'ACC002', 'ACC003'   # Accesorios
    ]
    
    with app.app_context():
        productos_eliminados = 0
        productos_no_encontrados = 0
        
        print("🧹 LIMPIANDO PRODUCTOS DE EJEMPLO DEL INVENTARIO")
        print("=" * 50)
        
        for codigo in codigos_ejemplo:
            producto = Product.query.filter_by(code=codigo).first()
            
            if producto:
                print(f"🗑️  Eliminando: {codigo} - {producto.name}")
                db.session.delete(producto)
                productos_eliminados += 1
            else:
                productos_no_encontrados += 1
        
        try:
            db.session.commit()
            
            print("\n✅ LIMPIEZA COMPLETADA:")
            print(f"   🗑️  Productos eliminados: {productos_eliminados}")
            print(f"   ❓ Productos no encontrados: {productos_no_encontrados}")
            
            # Verificar productos restantes
            productos_restantes = Product.query.filter_by(active=True).count()
            print(f"   📦 Productos restantes en inventario: {productos_restantes}")
            
            if productos_restantes == 0:
                print("\n💡 INVENTARIO LIMPIO:")
                print("   ✅ No hay productos de ejemplo")
                print("   ✅ El reporte mostrará solo productos reales")
                print("   ✅ Si no hay productos, aparecerá mensaje informativo")
            else:
                print("\n📋 PRODUCTOS REALES CONSERVADOS:")
                productos_reales = Product.query.filter_by(active=True).all()
                for p in productos_reales:
                    print(f"   📦 {p.code} - {p.name} ({p.category})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al limpiar productos: {e}")
            db.session.rollback()
            return False

def main():
    """Función principal"""
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if limpiar_productos_ejemplo():
        print("\n🎉 ¡LIMPIEZA EXITOSA!")
        print("\n📊 Ahora el reporte de inventario:")
        print("   ✅ Solo mostrará productos reales del inventario")
        print("   ✅ Si no hay productos, mostrará mensaje informativo")
        print("   ✅ Si hay productos, mostrará solo las categorías con datos")
        print("\n🔗 Prueba el reporte en:")
        print("   http://127.0.0.1:5001/reports")
        print("   Botón: 'Excel Inventario Pro'")
    else:
        print("❌ Error en la limpieza")

if __name__ == "__main__":
    main()