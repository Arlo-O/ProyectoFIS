from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioBoletin(RepositorioBase):
    """Repositorio para Boletin"""
    
    def __init__(self, db: Session):
        from ..modelos.boletin import Boletin
        super().__init__(db, Boletin)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene boletines de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
    
    def obtener_por_periodo(self, periodo_id: int):
        """Obtiene boletines de un período"""
        return self.filtrar(periodoId=periodo_id)
