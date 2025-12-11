from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioCitacion(RepositorioBase):
    """Repositorio para Citacion"""
    
    def __init__(self, db: Session):
        from ..modelos.citacion import Citacion
        super().__init__(db, Citacion)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene citaciones de un estudiante"""
        return self.filtrar(estudianteId=estudiante_id)
    
    def obtener_pendientes(self):
        """Obtiene citaciones pendientes"""
        return self.db.query(self.modelo).filter(
            self.modelo.estado == 'pendiente'
        ).all()
