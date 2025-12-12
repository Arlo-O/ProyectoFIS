
from datetime import datetime
from .persona import Persona

class Acudiente(Persona):
    """Acudiente que hereda de Persona (con asociación a Usuario)"""
    
    def __init__(self, id_acudiente: int, parentesco: str = None,
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
        
        self.id_acudiente = id_acudiente
        self.parentesco = parentesco
        
        # Asociación con Usuario (no herencia)
        self.usuario = None
        
        # Relationships
        self.estudiantes = []
        self.notificaciones = []
