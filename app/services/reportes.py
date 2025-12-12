from typing import List, TypedDict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import os
from datetime import datetime


class Calificacion(TypedDict):
    logro_titulo: str
    puntuacion: str
    comentarios: str


class ServicioReportes:
    
    def __init__(self, output_dir: str = "reportes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generar_boletin_pdf(self, estudiante_nombre: str, periodo: str, calificaciones: List[Calificacion]) -> str:
        filename = f"boletin_{estudiante_nombre.replace(' ', '_')}_{periodo.replace('/', '-')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph(f"<b>Boletín de Calificaciones</b><br/><br/>", styles['Title']))
        story.append(Paragraph(f"Estudiante: <b>{estudiante_nombre}</b>", styles['Normal']))
        story.append(Paragraph(f"Período: <b>{periodo}</b>", styles['Normal']))
        story.append(Paragraph(f"Fecha: <b>{datetime.now().strftime('%d/%m/%Y')}</b>", styles['Normal']))
        story.append(Spacer(1, 20))
        
        data = [["Logro", "Puntuación", "Comentarios"]]
        for cal in calificaciones:
            data.append([cal["logro_titulo"], cal["puntuacion"], cal.get("comentarios", "")])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)
        doc.build(story)
        return filepath

    def generar_listado_estudiantes_pdf(self, grupo_nombre: str, estudiantes: List[dict]) -> str:
        filename = f"listado_{grupo_nombre.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph(f"<b>Listado de Estudiantes</b><br/><br/>", styles['Title']))
        story.append(Paragraph(f"Grupo: <b>{grupo_nombre}</b>", styles['Normal']))
        story.append(Spacer(1, 20))
        
        data = [["#", "Nombre Completo", "Código Matrícula"]]
        for i, est in enumerate(estudiantes, 1):
            data.append([str(i), est.get("nombre_completo", ""), est.get("codigo_matricula", "")])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)
        doc.build(story)
        return filepath

    def generar_logros_pdf(self, estudiante_nombre: str, logros: List[Calificacion]) -> str:
        filename = f"logros_{estudiante_nombre.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph(f"<b>Reporte de Logros</b><br/><br/>", styles['Title']))
        story.append(Paragraph(f"Estudiante: <b>{estudiante_nombre}</b>", styles['Normal']))
        story.append(Spacer(1, 20))
        
        data = [["Logro", "Puntuación"]]
        for logro in logros:
            data.append([logro["logro_titulo"], logro["puntuacion"]])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)
        doc.build(story)
        return filepath
