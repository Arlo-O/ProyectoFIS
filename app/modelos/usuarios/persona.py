from datetime import datetime
from typing import Optional


class Persona:
    def __init__(self, numero_identificacion: str, tipo_identificacion: str, 
                 primer_nombre: str, segundo_nombre: Optional[str] = None,
                 primer_apellido: str = "", segundo_apellido: Optional[str] = None,
                 fecha_nacimiento: datetime = None, telefono: Optional[str] = None,
                 direccion: Optional[str] = None, genero: Optional[str] = None):
        self._numero_identificacion = numero_identificacion
        self._tipo_identificacion = tipo_identificacion
        self._primer_nombre = primer_nombre
        self._segundo_nombre = segundo_nombre
        self._primer_apellido = primer_apellido
        self._segundo_apellido = segundo_apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._telefono = telefono
        self._direccion = direccion
        self._genero = genero

    @property
    def numero_identificacion(self) -> str:
        return self._numero_identificacion

    @property
    def tipo_identificacion(self) -> str:
        return self._tipo_identificacion

    @property
    def primer_nombre(self) -> str:
        return self._primer_nombre

    @property
    def segundo_nombre(self) -> Optional[str]:
        return self._segundo_nombre

    @property
    def primer_apellido(self) -> str:
        return self._primer_apellido

    @property
    def segundo_apellido(self) -> Optional[str]:
        return self._segundo_apellido

    @property
    def fecha_nacimiento(self) -> Optional[datetime]:
        return self._fecha_nacimiento

    @property
    def telefono(self) -> Optional[str]:
        return self._telefono

    @property
    def direccion(self) -> Optional[str]:
        return self._direccion

    @property
    def genero(self) -> Optional[str]:
        return self._genero
