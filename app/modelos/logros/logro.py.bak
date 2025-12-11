from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from ..logros.categoriaLogro import CategoriaLogro


class Logro:
    def __init__(self, id_logro: int, titulo: str, descripcion: str, 
                 fecha_creacion: datetime, estado: str, id_creador: Optional[int] = None,
                 id_categoria: Optional[int] = None):
        self.__id_logro = id_logro
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__fecha_creacion = fecha_creacion
        self.__estado = estado
        self.__id_creador = id_creador
        self.__id_categoria = id_categoria

    @property
    def id_logro(self) -> int:
        return self.__id_logro

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, value: str) -> None:
        self.__titulo = value

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, value: str) -> None:
        self.__descripcion = value

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    @property
    def estado(self) -> str:
        return self.__estado

    @estado.setter
    def estado(self, value: str) -> None:
        self.__estado = value

    @property
    def id_creador(self) -> Optional[int]:
        return self.__id_creador

    @property
    def id_categoria(self) -> Optional[int]:
        return self.__id_categoria
