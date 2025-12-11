from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioDirectivo(RepositorioBase):
    """Repositorio para Directivo"""
    
    def __init__(self, db: Session):
        from ..modelos.directivo import Directivo
        super().__init__(db, Directivo)
