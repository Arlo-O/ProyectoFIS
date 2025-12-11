from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioEntrevista(RepositorioBase):
    """Repositorio para Entrevista"""
    
    def __init__(self, db: Session):
        from ..modelos.entrevista import Entrevista
        super().__init__(db, Entrevista)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene entrevistas de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
