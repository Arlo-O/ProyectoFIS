
from datetime import datetime

class Rol:
    """Rol del sistema para control de permisos"""
    
    def __init__(self, id_rol: int, nombre: str, descripcion: str = None,
                 fecha_creacion: datetime = None, fecha_actualizacion: datetime = None):
        self.id_rol = id_rol
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion or datetime.utcnow()
        self.fecha_actualizacion = fecha_actualizacion or datetime.utcnow()
        
        # Relationships
        self.usuarios = []
        self.permisos = []
