
from datetime import datetime
from .usuario import Usuario

class Directivo(Usuario):
    """Directivo que hereda de Usuario"""
    
    def __init__(self, id_directivo: int, cargo: str = None, area_responsable: str = None,
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
        
        self.id_directivo = id_directivo
        self.cargo = cargo
        self.area_responsable = area_responsable
        
        # Relationships
        self.logros_creados = []
        self.categorias_creadas = []
        self.entrevistas = []
        self.citaciones = []
