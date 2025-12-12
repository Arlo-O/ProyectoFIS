
from datetime import datetime
from .persona import Persona

class Estudiante(Persona):
    """Estudiante que hereda de Persona (NO de Usuario)"""
    
    def __init__(self, id_estudiante: int, codigo_matricula: str = None,
                 fecha_ingreso: datetime = None, grado_actual: str = None,
                 id_grupo: int = None,
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
        
        self.id_estudiante = id_estudiante
        self.codigo_matricula = codigo_matricula
        self.fecha_ingreso = fecha_ingreso
        self.grado_actual = grado_actual
        self.id_grupo = id_grupo
        
        # Relationships
        self.grupo = None
        self.acudientes = []
        self.hoja_vida = None
        self.observador = None
        self.evaluaciones = []
        self.boletines = []

        
        self.id_estudiante = id_estudiante
        self.codigo_matricula = codigo_matricula
        self.fecha_ingreso = fecha_ingreso
        self.grado_actual = grado_actual
        self.id_grupo = id_grupo
        
        # Relationships
        self.grupo = None
        self.acudientes = []
        self.hoja_vida = None
        self.observador = None
        self.evaluaciones = []
        self.boletines = []
