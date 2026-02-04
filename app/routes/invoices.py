from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import db
from app.models.models import Product, Customer
from app.models.transactions import Invoice, InvoiceItem
from datetime import datetime

bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@bp.route('/')
@login_required
def index():
    """Página principal de facturación"""
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    customers = Customer.query.filter_by(active=True).all()
    products = Product.query.filter_by(active=True).all()
    
    # Convertir productos a diccionarios para JSON
    products_dict = [p.to_dict() for p in products]
    
    return render_template('invoices/index.html', 
                         invoices=invoices,
                         customers=customers,
                         products=products_dict)

@bp.route('/api/invoices')
@login_required
def get_invoices():
    """API: Obtener todas las facturas"""
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return jsonify([i.to_dict() for i in invoices])

@bp.route('/api/invoices/<int:invoice_id>')
@login_required
def get_invoice(invoice_id):
    """API: Obtener una factura específica"""
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice.to_dict())

@bp.route('/api/invoices', methods=['POST'])
@login_required
def create_invoice():
    """API: Crear nueva factura"""
    data = request.get_json()
    
    customer = Customer.query.get(data['customer_id'])
    
    # Crear factura
    invoice = Invoice(
        invoice_number=f"FAC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        customer_id=customer.id,
        customer_name=customer.name,
        payment_method=data['payment_method'],
        notes=data.get('notes', '')
    )
    
    db.session.add(invoice)
    db.session.flush()
    
    # Agregar items
    for item_data in data['items']:
        product = Product.query.get(item_data['product_id'])
        
        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=product.id,
            product_name=product.name,
            product_code=product.code,
            quantity=item_data['quantity'],
            unit_price=product.sell_price
        )
        item.calculate_line_total()
        db.session.add(item)
    
    # Calcular totales
    invoice.calculate_totals()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Factura creada exitosamente',
        'invoice': invoice.to_dict()
    }), 201

@bp.route('/api/invoices/<int:invoice_id>/status', methods=['PUT'])
@login_required
def update_invoice_status(invoice_id):
    """API: Actualizar estado de factura"""
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()
    
    invoice.status = data['status']
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Estado actualizado exitosamente'
    })

@bp.route('/api/invoices/<int:invoice_id>/pay', methods=['POST'])
@login_required
def mark_as_paid(invoice_id):
    """API: Marcar factura como pagada"""
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = 'paid'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Factura marcada como pagada'
    })

@bp.route('/api/invoices/<int:invoice_id>/pdf')
@login_required
def download_pdf(invoice_id):
    """API: Generar PDF profesional de factura"""
    from flask import make_response
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from io import BytesIO
    import os
    
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Crear PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Contenedor para elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Logo y encabezado (si existe logo)
    logo_path = 'f:/Libreria JODA/logo/logo.png'
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1.5*inch, height=1.5*inch)
            elements.append(img)
            elements.append(Spacer(1, 12))
        except:
            pass
    
    # Título
    elements.append(Paragraph("LIBRERÍA JODA", title_style))
    elements.append(Spacer(1, 12))
    
    # Información de la empresa
    company_info = [
        ["RFC: JODA", "FACTURA"],
        ["Dirección: San Salvador, El Salvador", f"No. {invoice.invoice_number}"],
        ["Tel: (503) 7946-8807", f"Fecha: {invoice.created_at.strftime('%d/%m/%Y %H:%M')}"],
        ["Email: info@libreriajoda.com", ""]
    ]
    
    info_table = Table(company_info, colWidths=[3.5*inch, 2.5*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (1, 0), (1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 0), (1, 1), 12),
        ('TEXTCOLOR', (1, 0), (1, 1), colors.HexColor('#2563eb')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Información del cliente
    elements.append(Paragraph("DATOS DEL CLIENTE", heading_style))
    
    # Crear tabla para información del cliente
    customer_data = [
        ["Cliente:", invoice.customer_name],
        ["Estado:", invoice.status.upper()],
        ["Método de Pago:", invoice.payment_method.upper()]
    ]
    
    customer_table = Table(customer_data, colWidths=[1.5*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(customer_table)
    
    elements.append(Spacer(1, 20))
    
    # Tabla de productos
    elements.append(Paragraph("DETALLE DE PRODUCTOS", heading_style))
    
    # Encabezados de tabla
    table_data = [['Código', 'Producto', 'Cant.', 'Precio Unit.', 'Total']]
    
    # Items
    for item in invoice.items:
        table_data.append([
            item.product_code,
            item.product_name,
            str(item.quantity),
            f"${item.unit_price:,.2f}",
            f"${item.line_total:,.2f}"
        ])
    
    # Crear tabla
    products_table = Table(table_data, colWidths=[1*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    products_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(products_table)
    elements.append(Spacer(1, 20))
    
    # Totales - Solo mostrar total sin IVA
    totals_data = [
        ['', '', '', 'TOTAL A PAGAR:', f"${invoice.total:,.2f}"]
    ]
    
    totals_table = Table(totals_data, colWidths=[1*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, 0), (4, 0), 12),
        ('TEXTCOLOR', (3, 0), (4, 0), colors.HexColor('#2563eb')),
        ('LINEABOVE', (3, 0), (4, 0), 2, colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(totals_table)
    
    # Notas
    if invoice.notes:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Notas:", heading_style))
        elements.append(Paragraph(invoice.notes, normal_style))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Gracias por su preferencia - LIBRERÍA JODA", footer_style))
    elements.append(Paragraph("Documento generado electrónicamente", footer_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta con headers mejorados
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="factura_{invoice.invoice_number}.pdf"'
    response.headers['Content-Length'] = len(pdf)
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    
    return response
