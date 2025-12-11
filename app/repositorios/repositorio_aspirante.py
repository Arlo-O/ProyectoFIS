from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioAspirante(RepositorioBase):
    """Repositorio para Aspirante"""
    
    def __init__(self, db: Session):
        from ..modelos.aspirante import Aspirante
        super().__init__(db, Aspirante)
    
    def obtener_por_estado(self, estado: str):
        """Obtiene aspirantes por estado"""
        return self.filtrar(estado=estado)
