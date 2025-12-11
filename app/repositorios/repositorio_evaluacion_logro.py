from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioEvaluacionLogro(RepositorioBase):
    """Repositorio para EvaluacionLogro"""
    
    def __init__(self, db: Session):
        from ..modelos.evaluacionLogro import EvaluacionLogro
        super().__init__(db, EvaluacionLogro)
    
    def obtener_por_evaluacion(self, evaluacion_id: int):
        """Obtiene evaluaciones de logros de una evaluación"""
        return self.filtrar(evaluacionId=evaluacion_id)
    
    def obtener_por_logro(self, logro_id: int):
        """Obtiene evaluaciones de un logro"""
        return self.filtrar(logroId=logro_id)
