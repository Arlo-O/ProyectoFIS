
from datetime import datetime
from .usuario import Usuario

class Profesor(Usuario):
    """Profesor que hereda de Usuario"""
    
    def __init__(self, id_profesor: int, especialidad: str = None,
                 experiencia_anios: int = None, es_director_grupo: bool = False,
                 # Parámetros de Usuario
                 id_usuario: int = None, correo_electronico: str = None,
                 contrasena: str = None, id_rol: int = None, activo: bool = True,
                 ultimo_ingreso: datetime = None,
                 # Parámetros de Persona
                 id_persona: int = None, tipo_identificacion: str = None,
                 numero_identificacion: str = None, primer_nombre: str = None,
                 segundo_nombre: str = None, primer_apellido: str = None,
                 segundo_apellido: str = None, fecha_nacimiento: datetime = None,
                 genero: str = None, direccion: str = None, telefono: str = None):
        
        super().__init__(
            id_usuario=id_usuario,
            correo_electronico=correo_electronico,
            contrasena=contrasena,
            id_rol=id_rol,
            activo=activo,
            ultimo_ingreso=ultimo_ingreso,
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
        
        self.id_profesor = id_profesor
        self.especialidad = especialidad
        self.experiencia_anios = experiencia_anios
        self.es_director_grupo = es_director_grupo
        
        # Relationships
        self.grupos = []
        self.grupos_dirigidos = []
        self.evaluaciones = []
        self.boletines = []
        self.anotaciones = []
        self.entrevistas = []
