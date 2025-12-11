from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioGrado(RepositorioBase):
    """Repositorio para Grado"""
    
    def __init__(self, db: Session):
        from ..modelos.grado import Grado
        super().__init__(db, Grado)
    
    def obtener_por_nombre(self, nombre: str):
        """Obtiene un grado por nombre"""
        return self.db.query(self.modelo).filter(
            self.modelo.nombre == nombre
        ).first()
