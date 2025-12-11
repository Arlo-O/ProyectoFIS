from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioEvaluacion(RepositorioBase):
    """Repositorio para Evaluacion"""
    
    def __init__(self, db: Session):
        from ..modelos.evaluacion import Evaluacion
        super().__init__(db, Evaluacion)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene evaluaciones de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
    
    def obtener_por_periodo(self, periodo_id: int):
        """Obtiene evaluaciones de un período"""
        return self.filtrar(periodoId=periodo_id)
