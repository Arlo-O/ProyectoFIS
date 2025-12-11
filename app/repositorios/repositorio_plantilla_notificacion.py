from sqlalchemy.orm import Session
from .repositorio_base import RepositorioBase


class RepositorioPlantillaNotificacion(RepositorioBase):
    """Repositorio para PlantillaNotificacion"""
    
    def __init__(self, db: Session):
        from ..modelos.plantillaNotificacion import PlantillaNotificacion
        super().__init__(db, PlantillaNotificacion)
    
    def obtener_por_nombre(self, nombre: str):
        """Obtiene una plantilla por nombre"""
        return self.db.query(self.modelo).filter(
            self.modelo.nombre == nombre
        ).first()
