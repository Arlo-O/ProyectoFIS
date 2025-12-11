from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioNotificacion(RepositorioBase):
    """Repositorio para Notificacion"""
    
    def __init__(self, db: Session):
        from ..modelos.notificacion import Notificacion
        super().__init__(db, Notificacion)
    
    def obtener_por_usuario(self, usuario_id: int):
        """Obtiene notificaciones de un usuario"""
        return self.filtrar(usuarioId=usuario_id)
    
    def obtener_no_leidas(self, usuario_id: int):
        """Obtiene notificaciones no leídas"""
        return self.db.query(self.modelo).filter(
            (self.modelo.usuarioId == usuario_id) &
            (self.modelo.leida == False)
        ).all()
