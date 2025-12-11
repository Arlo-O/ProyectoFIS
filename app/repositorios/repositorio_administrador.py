from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioAdministrador(RepositorioBase):
    """Repositorio para Administrador"""
    
    def __init__(self, db: Session):
        from ..modelos.administrador import Administrador
        super().__init__(db, Administrador)
