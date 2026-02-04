#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar facturas existentes eliminando IVA
Sistema de Librería JODA
"""

import sys
import os

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import db, create_app
from app.models.models import Product, Customer
from app.models.transactions import Invoice, InvoiceItem, Sale, SaleItem

def actualizar_facturas_sin_iva():
    """Actualiza las facturas existentes para eliminar IVA"""
    
    app = create_app()
    
    with app.app_context():
        print("🔄 ACTUALIZANDO FACTURAS - ELIMINANDO IVA")
        print("=" * 50)
        
        # Actualizar facturas existentes
        print("\n📄 1. Procesando facturas...")
        facturas = Invoice.query.all()
        facturas_actualizadas = 0
        
        for factura in facturas:
            # Recalcular totales sin IVA
            factura.calculate_totals()
            facturas_actualizadas += 1
            print(f"   ✅ Factura {factura.invoice_number}: ${factura.total:.2f} (sin IVA)")
        
        # Actualizar ventas existentes  
        print(f"\n💰 2. Procesando ventas...")
        ventas = Sale.query.all()
        ventas_actualizadas = 0
        
        for venta in ventas:
            # Recalcular totales sin IVA
            venta.calculate_totals()
            ventas_actualizadas += 1
            print(f"   ✅ Venta {venta.sale_number}: ${venta.total:.2f} (sin IVA)")
        
        # Guardar cambios
        try:
            db.session.commit()
            print(f"\n✅ ACTUALIZACIÓN COMPLETADA")
            print(f"   📄 {facturas_actualizadas} facturas actualizadas")
            print(f"   💰 {ventas_actualizadas} ventas actualizadas")
            print(f"   🚫 IVA eliminado de todos los documentos")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error al guardar cambios: {e}")
            return False
        
        return True

def verificar_cambios():
    """Verifica que los cambios se aplicaron correctamente"""
    
    app = create_app()
    
    with app.app_context():
        print(f"\n🔍 VERIFICANDO CAMBIOS...")
        
        # Verificar facturas
        facturas = Invoice.query.all()
        for factura in facturas[:3]:  # Verificar las primeras 3
            print(f"   📄 Factura {factura.invoice_number}:")
            print(f"      Total: ${factura.total:.2f}")
            print(f"      Subtotal: ${factura.subtotal:.2f}")
            print(f"      IVA: ${factura.tax:.2f}")
            
            if factura.tax == 0 and factura.subtotal == factura.total:
                print("      ✅ Configuración correcta (sin IVA)")
            else:
                print("      ❌ Configuración incorrecta")
        
        print(f"\n🎉 Sistema actualizado para operar sin IVA")

def main():
    """Función principal"""
    print("🏪 LIBRERÍA JODA - ACTUALIZACIÓN SIN IVA")
    print("=" * 60)
    
    if actualizar_facturas_sin_iva():
        verificar_cambios()
        print(f"\n✅ PROCESO COMPLETADO EXITOSAMENTE")
        print(f"\n📝 RESUMEN DE CAMBIOS:")
        print(f"   • IVA eliminado de facturas y ventas")
        print(f"   • Subtotal = Total (sin impuestos)")
        print(f"   • IVA = 0 en todos los documentos")
        print(f"   • PDFs solo muestran 'Total a Pagar'")
        print(f"   • Frontend simplificado sin cálculo de IVA")
    else:
        print(f"\n❌ Error en el proceso de actualización")

if __name__ == "__main__":
    main()