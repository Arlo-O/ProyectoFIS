
from datetime import datetime

class Rol:
    """Rol del sistema para control de permisos"""
    
    def __init__(self, id_rol: int = None, nombre_rol: str = None, descripcion_rol: str = None):
        self.id_rol = id_rol
        self.nombre_rol = nombre_rol  # ✅ Correcto con _rol
        self.descripcion_rol = descripcion_rol  # ✅ Correcto con _rol
        
        # Relationships
        self.usuarios = []
        self.permisos = []
