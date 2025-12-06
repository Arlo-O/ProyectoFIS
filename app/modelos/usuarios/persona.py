from abc import ABC, abstractmethod
from datetime import datetime

class Persona(ABC):
    def __init__(self, primerNombre: str, segundoNombre : str, primerApellido : str, segundoApellido: str, 
                tipoDocumento: str, numeroDocumento: str, fechaNacimiento: datetime, genero: str,
                direccion: str, telefono: str):
        self._primerNombre = primerNombre
        self._segundoNombre = segundoNombre
        self._primerApellido = primerApellido
        self._segundoApellido = segundoApellido
        self._tipoDocumento = tipoDocumento
        self._numeroDocumento = numeroDocumento
        self._fechaNacimiento = fechaNacimiento
        self._genero = genero
        self._direccion = direccion
        self._telefono = telefono

    @property
    def primerNombre(self) -> str:
        return self._primerNombre

    @property
    def segundoNombre(self) -> str:
        return self._segundoNombre

    @property
    def primerApellido(self) -> str:
        return self._primerApellido

    @property
    def segundoApellido(self) -> str:
        return self._segundoApellido

    @property
    def tipoDocumento(self) -> str:
        return self._tipoDocumento

    @property
    def numeroDocumento(self) -> str:
        return self._numeroDocumento

    @property
    def fechaNacimiento(self) -> datetime:
        return self._fechaNacimiento

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def telefono(self) -> str:
        return self._telefono

    def obtenerNombreCompleto(self) -> str:
        partes = [
            self._primerNombre,
            self._segundoNombre,
            self._primerApellido,
            self._segundoApellido
        ]
        return " ".join([p for p in partes if p])
    
    def calcularEdad(self) -> int:
        return int(datetime.now().year - self._fechaNacimiento.year)

    