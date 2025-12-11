from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from .grupo import Grupo


class Grado:
    def __init__(self, id_grado: int, nombre: str):
        self.__id_grado = id_grado
        self.__nombre = nombre
        self.__grupos: List['Grupo'] = []

    @property
    def id_grado(self) -> int:
        return self.__id_grado

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def grupos(self) -> List['Grupo']:
        return self.__grupos.copy()

    def agregar_grupo(self, grupo: 'Grupo') -> None:
        if grupo not in self.__grupos:
            self.__grupos.append(grupo)

    def eliminar_grupo(self, grupo: 'Grupo') -> None:
        if grupo in self.__grupos:
            self.__grupos.remove(grupo)
