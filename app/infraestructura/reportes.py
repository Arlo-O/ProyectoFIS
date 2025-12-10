from typing import List, Any
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Módulo para la generación de reportes en formato PDF
# Utiliza la biblioteca ReportLab para la creación de documentos PDF

class ServicioReportes:
    """
    Servicio para la generación de reportes en formato PDF.
    Permite crear diferentes tipos de reportes como boletines de calificaciones,
    listados de estudiantes y registros de logros.
    """
    
    def __init__(self, output_dir: str = "reportes"):
        """
        Inicializa el servicio de reportes.
        
        Args:
            output_dir: Directorio donde se guardarán los reportes generados
        """
        self.output_dir = output_dir
        # Crea el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generar_boletin_pdf(self, estudiante_nombre: str, periodo: str, calificaciones: List[Any]) -> str:
        """
        Genera un boletín de calificaciones en formato PDF.
        
        Args:
            estudiante_nombre: Nombre completo del estudiante
            periodo: Período académico del boletín
            calificaciones: Lista de calificaciones del estudiante
            
        Returns:
            str: Ruta completa al archivo PDF generado
        """
        # Genera un nombre de archivo único basado en el nombre del estudiante y el período
        filename = f"boletin_{estudiante_nombre.replace(' ', '_')}_{periodo}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crea un nuevo documento PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        
        # Encabezado del boletín
        c.drawString(100, 750, f"Boletín de Calificaciones - {periodo}")
        c.drawString(100, 730, f"Estudiante: {estudiante_nombre}")
        
        # Lista de calificaciones
        y = 700  # Posición vertical inicial
        for cal in calificaciones:
            # Obtiene el título del logro y la puntuación, con valores por defecto
            logro_titulo = getattr(cal.logro, 'titulo', 'Logro sin título')
            puntuacion = getattr(cal, 'puntuacion', 'N/A')
            
            # Agrega la calificación al PDF
            c.drawString(100, y, f"Logro: {logro_titulo} - Nota: {puntuacion}")
            y -= 20  # Reduce la posición vertical para la siguiente línea
            
        # Guarda el documento PDF
        c.save()
        return filepath

    def generar_listado_estudiantes_pdf(self, grupo_nombre: str, estudiantes: List[Any]) -> str:
        """
        Genera un listado de estudiantes en formato PDF.
        
        Args:
            grupo_nombre: Nombre del grupo
            estudiantes: Lista de objetos de estudiantes
            
        Returns:
            str: Ruta completa al archivo PDF generado
        """
        # Genera un nombre de archivo único basado en el nombre del grupo
        filename = f"listado_{grupo_nombre.replace(' ', '_')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crea un nuevo documento PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        
        # Encabezado del listado
        c.drawString(100, 750, f"Listado de Estudiantes - Grupo {grupo_nombre}")
        
        # Lista de estudiantes
        y = 730  # Posición vertical inicial
        for est in estudiantes:
            # Obtiene el nombre completo del estudiante
            nombre = est.obtenerNombreCompleto()
            c.drawString(100, y, f"- {nombre}")
            y -= 20  # Reduce la posición vertical para el siguiente estudiante
            
        # Guarda el documento PDF
        c.save()
        return filepath

    def generar_logros_pdf(self, estudiante_nombre: str, logros: List[Any]) -> str:
        """
        Genera un reporte de logros en formato PDF.
        
        Args:
            estudiante_nombre: Nombre del estudiante
            logros: Lista de logros del estudiante
            
        Returns:
            str: Ruta completa al archivo PDF generado
        """
        # Genera un nombre de archivo único basado en el nombre del estudiante
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
