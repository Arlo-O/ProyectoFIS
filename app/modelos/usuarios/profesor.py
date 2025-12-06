from typing import List, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario
from .rol import Rol

if TYPE_CHECKING:
    from ..academico.grupo import Grupo

class Profesor(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idProfesor: int = None, esDirectorGrupo: bool = False):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idProfesor: int = idProfesor
        self.__esDirectorGrupo: bool = esDirectorGrupo
        self.__gruposAsignados: List['Grupo'] = []

    @property
    def idProfesor(self) -> int:
        return self.__idProfesor

    @property
    def correoInstitucional(self) -> str:
        return self.correoElectronico

    @property
    def esDirectorGrupo(self) -> bool:
        return self.__esDirectorGrupo

    @esDirectorGrupo.setter
    def esDirectorGrupo(self, valor: bool) -> None:
        self.__esDirectorGrupo = valor

    def obtenerGrupos(self) -> List['Grupo']:
        return self.__gruposAsignados.copy()

    def agregarGrupo(self, grupo: 'Grupo') -> None:
        if grupo not in self.__gruposAsignados:
            self.__gruposAsignados.append(grupo)

    def eliminarGrupo(self, grupo: 'Grupo') -> None:
        if grupo in self.__gruposAsignados:
            self.__gruposAsignados.remove(grupo)