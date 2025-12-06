from datetime import datetime
from .usuario import Usuario
from .rol import Rol

class Directivo(Usuario):
    def __init__(self, primerNombre: str, segundoNombre: str, primerApellido: str, segundoApellido: str,
                 tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                 direccion: str, telefono: str, correoElectronico: str, rol: Rol, contrasena: str,
                 idDirectivo: int = None, cargo: str = None, areaResponsable: str = None):
        super().__init__(primerNombre, segundoNombre, primerApellido, segundoApellido,
                         tipoDocumento, numeroDocumento, fechaNacimiento, genero, direccion, telefono,
                         correoElectronico, rol, contrasena)
        self.__idDirectivo: int = idDirectivo
        self.__cargo: str = cargo
        self.__areaResponsable: str = areaResponsable

    @property
    def idDirectivo(self) -> int:
        return self.__idDirectivo

    @property
    def cargo(self) -> str:
        return self.__cargo

    @property
    def areaResponsable(self) -> str:
        return self.__areaResponsable

    @idDirectivo.setter
    def idDirectivo(self, nuevoId: int) -> None:
        self.__idDirectivo = nuevoId

    @cargo.setter
    def cargo(self, nuevoCargo: str) -> None:
        self.__cargo = nuevoCargo

    @areaResponsable.setter
    def areaResponsable(self, nuevaArea: str) -> None:
        self.__areaResponsable = nuevaArea

    def obtenerInformacion(self) -> str:
        return f"Directivo {self.obtenerNombreCompleto()} - {self.__cargo or ''}"