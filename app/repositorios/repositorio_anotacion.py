from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioAnotacion(RepositorioBase):
    """Repositorio para Anotacion"""
    
    def __init__(self, db: Session):
        from ..modelos.anotacion import Anotacion
        super().__init__(db, Anotacion)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene anotaciones de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
    
    def obtener_por_tipo(self, tipo: str):
        """Obtiene anotaciones por tipo"""
        return self.filtrar(tipo=tipo)
