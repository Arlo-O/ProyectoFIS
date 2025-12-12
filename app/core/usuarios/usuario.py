
from datetime import datetime

class Usuario:
    """
    Clase Usuario (ASOCIACIÓN, NO HERENCIA)
    
    Usuario es una tabla independiente que representa credenciales de acceso al sistema.
    Relación: Los que tienen usuario son: Directivo, Profesor, Acudiente (como asociación)
    Administrador es especial - hereda de Persona y tiene usuario integrado
    Estudiante NO tiene usuario, solo Persona
    """
    
    def __init__(self, id_usuario: int = None, correo_electronico: str = None, 
                 contrasena: str = None, id_rol: int = None, activo: bool = True,
                 ultimo_ingreso: datetime = None, fecha_creacion: datetime = None,
                 justificacion_inhabilitacion: str = None):
        
        self.id_usuario = id_usuario
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
        self.id_rol = id_rol
        self.activo = activo
        self.ultimo_ingreso = ultimo_ingreso
        self.fecha_creacion = fecha_creacion or datetime.utcnow()
        self.justificacion_inhabilitacion = justificacion_inhabilitacion
        
        # Relationships
        self.rol = None
        
        # Relación con la persona (se carga desde SQLAlchemy)
        # La persona que corresponde a este usuario se carga vía una relación ORM
        self.persona = None
