from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioPermiso(RepositorioBase):
    """Repositorio para Permiso"""
    
    def __init__(self, db: Session):
        from ..modelos.permiso import Permiso
        super().__init__(db, Permiso)
    
    def obtener_por_usuario(self, usuario_id: int):
        """Obtiene permisos de un usuario"""
        return self.filtrar(usuarioId=usuario_id)
