#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar y crear cliente por defecto
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Customer

def verificar_clientes():
    app = create_app()
    
    with app.app_context():
        customers = Customer.query.filter_by(active=True).all()
        print(f'👥 Clientes activos: {len(customers)}')
        
        if customers:
            print('📋 Clientes existentes:')
            for c in customers[:5]:
                print(f'   • {c.name} ({c.customer_type})')
        else:
            print('⚠️  No hay clientes activos, creando cliente por defecto...')
            # Crear cliente público general
            public_customer = Customer(
                name='Público General',
                email='publico@general.com',
                customer_type='regular',
                active=True
            )
            db.session.add(public_customer)
            db.session.commit()
            print('✅ Cliente "Público General" creado con ID 1')

if __name__ == "__main__":
    verificar_clientes()