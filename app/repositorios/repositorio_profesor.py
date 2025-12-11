from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioProfesor(RepositorioBase):
    """Repositorio para Profesor"""
    
    def __init__(self, db: Session):
        from ..modelos.profesor import Profesor
        super().__init__(db, Profesor)
    
    def obtener_por_especialidad(self, especialidad: str):
        """Obtiene profesores por especialidad"""
        return self.filtrar(especialidad=especialidad)
    
    def obtener_activos(self):
        """Obtiene profesores activos"""
        return self.db.query(self.modelo).filter(
            self.modelo.estado == 'activo'
        ).all()
