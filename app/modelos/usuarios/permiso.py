from datetime import datetime

class Permiso:
    """Permiso que puede asignarse a roles"""
    
    def __init__(self, id_permiso: int, nombre: str, descripcion: str = None,
                 fecha_creacion: datetime = None, fecha_actualizacion: datetime = None):
        self.id_permiso = id_permiso
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion or datetime.utcnow()
        self.fecha_actualizacion = fecha_actualizacion or datetime.utcnow()
        
        # Relationships
        self.roles = []