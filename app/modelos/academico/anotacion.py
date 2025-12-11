from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional


if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor


class Anotacion:
    def __init__(self, id_anotacion: int, fecha: datetime, descripcion: str, 
                 autor: Optional['Profesor'], tipo: str, id_observador: Optional[int] = None):
        self.__id_anotacion = id_anotacion
        self.__fecha = fecha
        self.__descripcion = descripcion
        self.__autor = autor
        self.__tipo = tipo
        self.__id_observador = id_observador

    @property
    def id_anotacion(self) -> int:
        return self.__id_anotacion

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def autor(self) -> Optional['Profesor']:
        return self.__autor

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def id_observador(self) -> Optional[int]:
        return self.__id_observador
