from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioEstudiante(RepositorioBase):
    """Repositorio para Estudiante"""
    
    def __init__(self, db: Session):
        from ..modelos.estudiante import Estudiante
        super().__init__(db, Estudiante)
    
    def obtener_por_grado(self, grado_id: int):
        """Obtiene estudiantes por grado"""
        return self.filtrar(gradoId=grado_id)
    
    def obtener_activos(self):
        """Obtiene estudiantes activos"""
        return self.db.query(self.modelo).filter(
            self.modelo.estado == 'activo'
        ).all()
