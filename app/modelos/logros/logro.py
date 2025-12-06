from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo

class Logro:
    def __init__(self, idLogro: int, titulo: str, descripcion: str, fechaCreacion: datetime, 
                 creador: 'Directivo', estado: str):
        self.__idLogro: int = idLogro
        self.__titulo: str = titulo
        self.__descripcion: str = descripcion
        self.__fechaCreacion: datetime = fechaCreacion
        self.__creador: 'Directivo' = creador
        self.__estado: str = estado

    @property
    def idLogro(self) -> int:
        return self.__idLogro

    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def fechaCreacion(self) -> datetime:
        return self.__fechaCreacion

    @property
    def creador(self) -> 'Directivo':
        return self.__creador

    @property
    def estado(self) -> str:
        return self.__estado

    @titulo.setter
    def titulo(self, nuevoTitulo: str) -> None:
        self.__titulo = nuevoTitulo

    @descripcion.setter
    def descripcion(self, nuevaDescripcion: str) -> None:
        self.__descripcion = nuevaDescripcion

    @estado.setter
    def estado(self, nuevoEstado: str) -> None:
        self.__estado = nuevoEstado

    def resumen(self) -> str:
        return f"{self.__descripcion} ({self.__estado})"