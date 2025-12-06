from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor

class Anotacion:
    def __init__(self, idAnotacion: int, fecha: datetime, descripcion: str, 
                 autor: 'Profesor', tipo: str):
        self.__idAnotacion: int = idAnotacion
        self.__fecha: datetime = fecha
        self.__descripcion: str = descripcion
        self.__autor: 'Profesor' = autor
        self.__tipo: str = tipo

    @property
    def idAnotacion(self) -> int:
        return self.__idAnotacion

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def autor(self) -> 'Profesor':
        return self.__autor

    @property
    def tipo(self) -> str:
        return self.__tipo