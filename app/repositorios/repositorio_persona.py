from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioPersona(RepositorioBase):
    """Repositorio para Persona"""
    
    def __init__(self, db: Session):
        from ..modelos.persona import Persona
        super().__init__(db, Persona)
    
    def obtener_por_numero_documento(self, numero_documento: str):
        """Obtiene una persona por número de documento"""
        return self.db.query(self.modelo).filter(
            self.modelo.numeroDocumento == numero_documento
        ).first()
