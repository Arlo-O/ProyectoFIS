from datetime import datetime
from .persona import Persona

class Estudiante(Persona):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, idEstudiante: int = None, grado: str = None, observaciones: list = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
        self.__idEstudiante: int = idEstudiante
        self.__grado: str = grado
        self.__observaciones: list = observaciones or []
        self.__boletines: list = []

    @property
    def idEstudiante(self) -> int:
        return self.__idEstudiante

    @property
    def grado(self) -> str:
        return self.__grado

    @property
    def observaciones(self) -> list:
        return self.__observaciones.copy()

    @idEstudiante.setter
    def idEstudiante(self, nuevoId: int) -> None:
        self.__idEstudiante = nuevoId

    @grado.setter
    def grado(self, nuevoGrado: str) -> None:
        self.__grado = nuevoGrado

    def agregarObservacion(self, observacion: str) -> None:
        self.__observaciones.append(observacion)

    def agregarBoletin(self, boletin) -> None:
        if boletin not in self.__boletines:
            self.__boletines.append(boletin)

    def removerBoletin(self, boletin) -> None:
        try:
            self.__boletines.remove(boletin)
        except ValueError:
            pass

    def obtenerBoletines(self) -> list:
        return self.__boletines.copy()