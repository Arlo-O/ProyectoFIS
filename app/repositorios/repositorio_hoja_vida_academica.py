from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioHojaVidaAcademica(RepositorioBase):
    """Repositorio para HojaVidaAcademica"""
    
    def __init__(self, db: Session):
        from ..modelos.hojaVidaAcademica import HojaVidaAcademica
        super().__init__(db, HojaVidaAcademica)
    
    def obtener_por_estudiante(self, estudiante_id: int):
        """Obtiene la hoja de vida académica de un estudiante"""
        return self.db.query(self.modelo).filter(
            self.modelo.estudianteId == estudiante_id
        ).first()
