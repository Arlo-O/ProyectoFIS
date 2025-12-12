
from datetime import datetime
from .usuario import Usuario

class Administrador(Usuario):
    """Administrador hereda de Usuario (única clase que hereda de Usuario)"""
    
    def __init__(self, id_administrador: int = None,
                 # Parámetros de Usuario
                 id_usuario: int = None, correo_electronico: str = None,
                 contrasena: str = None, id_rol: int = None, activo: bool = True,
                 ultimo_ingreso: datetime = None, fecha_creacion: datetime = None,
                 # Datos adicionales del administrador
                 primer_nombre: str = None, segundo_nombre: str = None,
                 primer_apellido: str = None, segundo_apellido: str = None,
                 telefono: str = None):
        
        super().__init__(
            id_usuario=id_usuario,
            correo_electronico=correo_electronico,
            contrasena=contrasena,
            id_rol=id_rol,
            activo=activo,
            ultimo_ingreso=ultimo_ingreso,
            fecha_creacion=fecha_creacion
        )
        
        self.id_administrador = id_administrador
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.telefono = telefono
