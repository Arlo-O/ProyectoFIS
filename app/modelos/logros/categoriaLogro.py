from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from .logro import Logro

class CategoriaLogro:
    def __init__(self, idCategoria: int, nombre: str, descripcion: str, creador: 'Directivo'):
        self.__idCategoria: int = idCategoria
        self.__nombre: str = nombre
        self.__descripcion: str = descripcion
        self.__creador: 'Directivo' = creador
        self.__logros: List['Logro'] = []

    @property
    def idCategoria(self) -> int:
        return self.__idCategoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def creador(self) -> 'Directivo':
        return self.__creador

    @property
    def logros(self) -> List['Logro']:
        return self.__logros.copy()

    def agregarLogro(self, logro: 'Logro') -> None:
        if logro not in self.__logros:
            self.__logros.append(logro)

    def eliminarLogro(self, logro: 'Logro') -> None:
        if logro in self.__logros:
            self.__logros.remove(logro)
