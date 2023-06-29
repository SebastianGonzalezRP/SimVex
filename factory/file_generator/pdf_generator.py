from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.validators import Auto


class PDFGenerator:
    def __init__(self,serial):
        
        self.doc = SimpleDocTemplate(f"files/{serial}/report.pdf", pagesize=letter)

        self.elements = []

        styles = getSampleStyleSheet()
        title = Paragraph(f"<b>Report {serial}</b>", styles['Title'])
        self.elements.append(title)

    def append_table(self,data):
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        
        self.elements.append(table) 


    def build_document(self):
        self.doc.build(self.elements)
