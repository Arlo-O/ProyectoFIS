
from datetime import datetime
from .persona import Persona  # ✅ IMPORT FALTANTE

class Usuario(Persona):
    """Clase Usuario que hereda de Persona (JOINED TABLE INHERITANCE)"""
    
    def __init__(self, id_usuario: int, correo_electronico: str, 
                 contrasena: str, id_rol: int = None, activo: bool = True,
                 ultimo_ingreso: datetime = None, fecha_creacion: datetime = None,
                 # Parámetros de Persona
                 id_persona: int = None, tipo_identificacion: str = None,
                 numero_identificacion: str = None, primer_nombre: str = None,
                 segundo_nombre: str = None, primer_apellido: str = None,
                 segundo_apellido: str = None, fecha_nacimiento: datetime = None,
                 genero: str = None, direccion: str = None, telefono: str = None):
        
        super().__init__(
            id_persona=id_persona,
            tipo_identificacion=tipo_identificacion,
            numero_identificacion=numero_identificacion,
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            direccion=direccion,
            telefono=telefono
        )
        
        self.id_usuario = id_usuario
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
        self.id_rol = id_rol
        self.activo = activo
        self.ultimo_ingreso = ultimo_ingreso
        self.fecha_creacion = fecha_creacion or datetime.utcnow()
        
        # Relationships
        self.rol = None
