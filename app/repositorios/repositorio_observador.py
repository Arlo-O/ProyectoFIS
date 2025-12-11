from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioObservador(RepositorioBase):
    """Repositorio para Observador"""
    
    def __init__(self, db: Session):
        from ..modelos.observador import Observador
        super().__init__(db, Observador)
