from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.validators import Auto


class PDFGenerator:
    def __init__(self,serial):
        
        self.doc = SimpleDocTemplate(f"files/{serial}/report.pdf", pagesize=letter)
        self.serial = serial

        self.elements = []

        styles = getSampleStyleSheet()
        title = Paragraph(f"<b>VexSim Report {serial}</b>", styles['Title'])
        self.elements.append(title)
        self.add_spacer()

    def append_subtitle(self,subtitle):
        subtitle_style = ParagraphStyle(name='SubtitleStyle',fontName = "Helvetica", fontSize=16, leading=18,spaceAfter=10)
        subtitle_paragraph = Paragraph(subtitle, style=subtitle_style)
        self.elements.append(subtitle_paragraph)

    def append_table(self,data,subtitle):
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                               ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                               ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        self.append_subtitle(subtitle)
        self.elements.append(table) 
        self.add_spacer()

    def append_graph(self,subtitle):
        self.append_subtitle(subtitle)
        image_path = "files/tmp/graph.png"
        image = Image(image_path, width=400, height=300)
        self.elements.append(image)
        self.add_spacer()
        

    def add_spacer(self):
        spacer = Spacer(1,20)
        self.elements.append(spacer)

    def build_document(self):
        self.doc.build(self.elements)
