from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioUsuario(RepositorioBase):
    """Repositorio para Usuario"""
    
    def __init__(self, db: Session):
        from ..modelos.usuario import Usuario
        super().__init__(db, Usuario)
    
    def obtener_por_email(self, email: str):
        """Obtiene un usuario por correo electrónico o username"""
        return self.db.query(self.modelo).filter(
            (self.modelo.correoElectronico == email) |
            (self.modelo.username == email)
        ).first()
    
    def obtener_por_username(self, username: str):
        """Obtiene un usuario por username"""
        return self.db.query(self.modelo).filter(
            self.modelo.username == username
        ).first()
    
    def obtener_activos(self):
        """Obtiene todos los usuarios activos"""
        return self.db.query(self.modelo).filter(
            self.modelo.activo == True
        ).all()

