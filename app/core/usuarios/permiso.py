from datetime import datetime

class Permiso:
    """Permiso que puede asignarse a roles"""
    
    def __init__(self, id_permiso: int, nombre: str, descripcion: str = None):
        self.id_permiso = id_permiso
        self.nombre = nombre
        self.descripcion = descripcion
        
        # Relationships
        self.roles = []