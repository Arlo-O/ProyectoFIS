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

    def nombreCompleto(self) -> str:
        return self._primerApellido + " " + self._segundoNombre + " " + self._primerApellido + " " + self._segundoApellido
    
    def calcularEdad(self) -> int:
        return int(datetime.now().year - self._fechaNacimiento.year)

    