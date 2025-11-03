from datetime import datetime
from .persona import Persona

class Acudiente(Persona):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, idAcudiente: int = None, parentesco: str = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
        self.__idAcudiente: int = idAcudiente
        self.__parentesco: str = parentesco
        self.__Representados: list = []

    @property
    def idAcudiente(self) -> int:
        return self.__idAcudiente

    @property
    def parentesco(self) -> str:
        return self.__parentesco

    @idAcudiente.setter
    def idAcudiente(self, nuevoId: int) -> None:
        self.__idAcudiente = nuevoId

    @parentesco.setter
    def parentesco(self, nuevoParentesco: str) -> None:
        self.__parentesco = nuevoParentesco

    def agregarEstudiante(self, estudiante) -> None:
        if estudiante not in self.__Representados:
            self.__Representados.append(estudiante)

    def removerEstudiante(self, estudiante) -> None:
        try:
            self.__Representados.remove(estudiante)
        except ValueError:
            pass

    def obtenerEstudiantes(self) -> list:
        return self.__Representados.copy()