from datetime import datetime
from .persona import Persona

class Directivo(Persona):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, idDirectivo: int = None, cargo: str = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono)
        self.__idDirectivo: int = idDirectivo
        self.__cargo: str = cargo

    @property
    def idDirectivo(self) -> int:
        return self.__idDirectivo

    @property
    def cargo(self) -> str:
        return self.__cargo

    @idDirectivo.setter
    def idDirectivo(self, nuevoId: int) -> None:
        self.__idDirectivo = nuevoId

    @cargo.setter
    def cargo(self, nuevoCargo: str) -> None:
        self.__cargo = nuevoCargo

    def asignarResponsabilidad(self, descripcion: str) -> None:
        # método para asignar una responsabilidad o tarea
        pass

    def obtenerInformacion(self) -> str:
        return f"Directivo {self.nombreCompleto()} - {self.__cargo or ''}"