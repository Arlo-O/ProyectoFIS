
from datetime import datetime

class Persona:
    """Clase base para toda persona en el sistema (JOINED TABLE INHERITANCE)"""
    
    def __init__(self, id_persona: int, tipo_identificacion: str, 
                 numero_identificacion: str, primer_nombre: str, 
                 segundo_nombre: str, primer_apellido: str, 
                 segundo_apellido: str, fecha_nacimiento: datetime = None,
                 genero: str = None, direccion: str = None, telefono: str = None):
        self.id_persona = id_persona
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.direccion = direccion
        self.telefono = telefono

    def nombre_completo(self) -> str:
        """Retorna el nombre completo de la persona"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        
        nombres_str = " ".join([n for n in nombres if n])
        apellidos_str = " ".join([a for a in apellidos if a])
        
        return f"{nombres_str} {apellidos_str}".strip()