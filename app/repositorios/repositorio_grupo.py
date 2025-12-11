from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioGrupo(RepositorioBase):
    """Repositorio para Grupo"""
    
    def __init__(self, db: Session):
        from ..modelos.grupo import Grupo
        super().__init__(db, Grupo)
    
    def obtener_por_grado(self, grado_id: int):
        """Obtiene grupos por grado"""
        return self.filtrar(gradoId=grado_id)
    
    def obtener_por_profesor(self, profesor_id: int):
        """Obtiene grupos asignados a un profesor"""
        return self.filtrar(profesorId=profesor_id)
