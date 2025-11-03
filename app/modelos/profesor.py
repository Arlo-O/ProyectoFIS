from datetime import datetime
from .persona import Persona

class Profesor(Persona):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, idProfesor: int = None, titulo: str = None, asignaturas: list = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
        self.__idProfesor: int = idProfesor
        self.__titulo: str = titulo
        self.__asignaturas: list = asignaturas or []

    @property
    def idProfesor(self) -> int:
        return self.__idProfesor

    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def asignaturas(self) -> list:
        return self.__asignaturas.copy()

    @idProfesor.setter
    def idProfesor(self, nuevoId: int) -> None:
        self.__idProfesor = nuevoId

    @titulo.setter
    def titulo(self, nuevoTitulo: str) -> None:
        self.__titulo = nuevoTitulo

    def agregarAsignatura(self, asignatura: str) -> None:
        if asignatura not in self.__asignaturas:
            self.__asignaturas.append(asignatura)

    def removerAsignatura(self, asignatura: str) -> None:
        try:
            self.__asignaturas.remove(asignatura)
        except ValueError:
            pass

    def obtenerInformacion(self) -> str:
        return f"Profesor {self.nombreCompleto()} - {self.__titulo or ''}"