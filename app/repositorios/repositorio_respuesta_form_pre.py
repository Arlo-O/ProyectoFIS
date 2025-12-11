from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioRespuestaFormPre(RepositorioBase):
    """Repositorio para RespuestaFormPre"""
    
    def __init__(self, db: Session):
        from ..modelos.respuestaFormPre import RespuestaFormPre
        super().__init__(db, RespuestaFormPre)
    
    def obtener_por_aspirante(self, aspirante_id: int):
        """Obtiene respuestas de un aspirante"""
        return self.filtrar(aspiranteId=aspirante_id)
