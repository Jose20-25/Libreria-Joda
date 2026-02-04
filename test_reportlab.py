#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de ReportLab para diagnóstico
"""

try:
    import reportlab
    print("✅ ReportLab importado correctamente")
    try:
        print(f"📦 Versión de ReportLab: {reportlab.Version}")
    except:
        print("📦 ReportLab instalado (versión no disponible)")
    
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from io import BytesIO
    
    print("✅ Todas las importaciones de ReportLab funcionan correctamente")
    
    # Test de creación de PDF básico
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Test PDF", styles['Title']))
    
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    print(f"✅ PDF de prueba generado: {len(pdf_data)} bytes")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()