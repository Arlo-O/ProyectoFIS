from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from .logro import Logro


class CategoriaLogro:
    def __init__(self, id_categoria: int, nombre: str, descripcion: str, 
                 id_creador: Optional[int] = None):
        self.__id_categoria = id_categoria
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__id_creador = id_creador
        self.__logros: List['Logro'] = []

    @property
    def id_categoria(self) -> int:
        return self.__id_categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def id_creador(self) -> Optional[int]:
        return self.__id_creador

    @property
    def logros(self) -> List['Logro']:
        return self.__logros.copy()
