from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioLogro(RepositorioBase):
    """Repositorio para Logro"""
    
    def __init__(self, db: Session):
        from ..modelos.logro import Logro
        super().__init__(db, Logro)
    
    def obtener_por_grado(self, grado_id: int):
        """Obtiene logros de un grado"""
        return self.filtrar(gradoId=grado_id)
    
    def obtener_por_asignatura(self, asignatura: str):
        """Obtiene logros de una asignatura"""
        return self.filtrar(asignatura=asignatura)
