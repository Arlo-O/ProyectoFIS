from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioAcudiente(RepositorioBase):
    """Repositorio para Acudiente"""
    
    def __init__(self, db: Session):
        from ..modelos.acudiente import Acudiente
        super().__init__(db, Acudiente)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene acudientes de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
