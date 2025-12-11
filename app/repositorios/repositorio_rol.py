from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioRol(RepositorioBase):
    """Repositorio para Rol"""
    
    def __init__(self, db: Session):
        from ..modelos.rol import Rol
        super().__init__(db, Rol)
    
    def obtener_por_nombre(self, nombre: str):
        """Obtiene un rol por nombre"""
        return self.db.query(self.modelo).filter(
            self.modelo.nombre == nombre
        ).first()
