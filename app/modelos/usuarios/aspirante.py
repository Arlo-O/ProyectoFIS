from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario
from .rol import Rol

if TYPE_CHECKING:
    from .acudiente import Acudiente
    from ..gestion.entrevista import Entrevista
    from ..academico.grupo import Grupo
    from .estudiante import Estudiante

class Aspirante(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idAspirante: int = None, gradoSolicitado: str = None, fechaSolicitud: datetime = None,
                 estadoProceso: str = "Preinscrito"):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idAspirante: int = idAspirante
        self.__gradoSolicitado: str = gradoSolicitado
        self.__fechaSolicitud: datetime = fechaSolicitud
        self.__estadoProceso: str = estadoProceso
        self.__acudientes: List['Acudiente'] = []
        self.__entrevista: Optional['Entrevista'] = None

    @property
    def idAspirante(self) -> int:
        return self.__idAspirante

    @property
    def gradoSolicitado(self) -> str:
        return self.__gradoSolicitado
    
    @property
    def fechaSolicitud(self) -> datetime:
        return self.__fechaSolicitud

    @property
    def estadoProceso(self) -> str:
        return self.__estadoProceso

    @property
    def entrevista(self) -> Optional['Entrevista']:
        return self.__entrevista

    @entrevista.setter
    def entrevista(self, nuevaEntrevista: 'Entrevista') -> None:
        self.__entrevista = nuevaEntrevista

    def solicitarEntrevista(self) -> bool:
        # Logic to change state or request interview
        if self.__estadoProceso == "Preinscrito":
            # Logic...
            return True
        return False

    def convertirAEstudiante(self, grupo: 'Grupo') -> 'Estudiante':
        # Logic to create Estudiante from Aspirante
        # This would likely be handled by a service, but method is here per dictionary.
        # Returning None as placeholder or need to import Estudiante inside method to avoid circular import if not using TYPE_CHECKING
        return None
