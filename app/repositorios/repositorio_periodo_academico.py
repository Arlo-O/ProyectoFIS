from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioPeriodoAcademico(RepositorioBase):
    """Repositorio para PeriodoAcademico"""
    
    def __init__(self, db: Session):
        from ..modelos.periodoAcademico import PeriodoAcademico
        super().__init__(db, PeriodoAcademico)
    
    def obtener_activo(self):
        """Obtiene el período académico activo"""
        return self.db.query(self.modelo).filter(
            self.modelo.activo == True
        ).first()
    
    def obtener_por_ano(self, ano: int):
        """Obtiene períodos de un año"""
        return self.filtrar(ano=ano)
