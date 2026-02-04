from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models.models import Product, Customer
from app.models.transactions import Sale
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def dashboard():
    """Dashboard principal"""
    # Estadísticas generales
    total_products = Product.query.filter_by(active=True).count()
    total_customers = Customer.query.filter_by(active=True).count()
    
    # Ventas del mes actual
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales = Sale.query.filter(Sale.created_at >= start_of_month).all()
    total_revenue = sum(sale.total for sale in monthly_sales)
    total_orders = len(monthly_sales)
    
    # Productos con stock bajo
    low_stock_products = Product.query.filter(
        Product.stock <= Product.min_stock,
        Product.active == True
    ).all()
    
    # Ventas recientes
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(10).all()
    
    # Datos para el gráfico (últimos 7 días)
    chart_data = []
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        day_sales = Sale.query.filter(
            Sale.created_at >= day_start,
            Sale.created_at <= day_end
        ).all()
        
        daily_total = sum(sale.total for sale in day_sales)
        chart_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'total': float(daily_total)
        })
    
    return render_template('dashboard.html',
                         total_revenue=total_revenue,
                         total_orders=total_orders,
                         total_products=total_products,
                         total_customers=total_customers,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales,
                         chart_data=chart_data)

@bp.route('/api/stats')
@login_required
def get_stats():
    """API para obtener estadísticas"""
    # Ventas del mes actual
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales = Sale.query.filter(Sale.created_at >= start_of_month).all()
    
    stats = {
        'total_revenue': sum(sale.total for sale in monthly_sales),
        'total_orders': len(monthly_sales),
        'total_products': Product.query.filter_by(active=True).count(),
        'total_customers': Customer.query.filter_by(active=True).count(),
        'low_stock_count': Product.query.filter(
            Product.stock <= Product.min_stock,
            Product.active == True
        ).count()
    }
    
    return jsonify(stats)
