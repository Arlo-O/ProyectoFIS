from typing import List, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario
from .rol import Rol

if TYPE_CHECKING:
    from .persona import Persona

class Acudiente(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idAcudiente: int = None, parentesco: str = None, esAspirante: bool = False):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idAcudiente: int = idAcudiente
        self.__parentesco: str = parentesco
        self.__esAspirante: bool = esAspirante
        self.__representados: List['Persona'] = []

    @property
    def idAcudiente(self) -> int:
        return self.__idAcudiente

    @property
    def parentesco(self) -> str:
        return self.__parentesco

    @property
    def esAspirante(self) -> bool:
        return self.__esAspirante

    @idAcudiente.setter
    def idAcudiente(self, nuevoId: int) -> None:
        self.__idAcudiente = nuevoId

    @parentesco.setter
    def parentesco(self, nuevoParentesco: str) -> None:
        self.__parentesco = nuevoParentesco

    @esAspirante.setter
    def esAspirante(self, valor: bool) -> None:
        self.__esAspirante = valor

    def obtenerRepresentados(self) -> List['Persona']:
        return self.__representados.copy()

    def agregarRepresentado(self, persona: 'Persona') -> None:
        if persona not in self.__representados:
            self.__representados.append(persona)