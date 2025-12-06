from typing import List, Any
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class ServicioReportes:
    def __init__(self, output_dir: str = "reportes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generar_boletin_pdf(self, estudiante_nombre: str, periodo: str, calificaciones: List[Any]) -> str:
        filename = f"boletin_{estudiante_nombre.replace(' ', '_')}_{periodo}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, f"Boletín de Calificaciones - {periodo}")
        c.drawString(100, 730, f"Estudiante: {estudiante_nombre}")
        
        y = 700
        for cal in calificaciones:
            # Assuming cal is an object with attributes or dict
            # Adjust based on actual EvaluacionLogro object structure
            logro_titulo = getattr(cal.logro, 'titulo', 'Logro sin título')
            puntuacion = getattr(cal, 'puntuacion', 'N/A')
            c.drawString(100, y, f"Logro: {logro_titulo} - Nota: {puntuacion}")
            y -= 20
            
        c.save()
        return filepath

    def generar_listado_estudiantes_pdf(self, grupo_nombre: str, estudiantes: List[Any]) -> str:
        filename = f"listado_{grupo_nombre.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, f"Listado de Estudiantes - Grupo {grupo_nombre}")
        
        y = 730
        for est in estudiantes:
            nombre = est.obtenerNombreCompleto()
            c.drawString(100, y, f"- {nombre}")
            y -= 20
            
        c.save()
        return filepath

    def generar_logros_pdf(self, estudiante_nombre: str, logros: List[Any]) -> str:
        filename = f"logros_{estudiante_nombre.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, f"Reporte de Logros - {estudiante_nombre}")
        
        y = 730
        for evaluacion in logros:
            titulo = evaluacion.logro.titulo
            nota = evaluacion.puntuacion
            c.drawString(100, y, f"{titulo}: {nota}")
            y -= 20
            
        c.save()
        return filepath
