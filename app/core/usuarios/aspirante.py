
from datetime import datetime
from .persona import Persona

class Aspirante(Persona):
    """Aspirante que hereda de Persona (con asociación a Usuario)"""
    
    def __init__(self, id_aspirante: int, grado_solicitado: str = None,
                 fecha_solicitud: datetime = None, estado_proceso: str = None,
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
        
        self.id_aspirante = id_aspirante
        self.grado_solicitado = grado_solicitado
        self.fecha_solicitud = fecha_solicitud
        self.estado_proceso = estado_proceso
        
        # Asociación con Usuario (no herencia)
        self.usuario = None
        
        # Relationships
        self.entrevista = None
