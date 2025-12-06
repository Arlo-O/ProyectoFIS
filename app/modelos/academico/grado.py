from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .grupo import Grupo

class Grado:
    def __init__(self, idGrado: int, nombre: str):
        self.__idGrado: int = idGrado
        self.__nombre: str = nombre
        self.__grupos: List['Grupo'] = []

    @property
    def idGrado(self) -> int:
        return self.__idGrado

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def grupos(self) -> List['Grupo']:
        return self.__grupos.copy()

    def agregarGrupo(self, grupo: 'Grupo') -> None:
        if grupo not in self.__grupos:
            self.__grupos.append(grupo)

    def eliminarGrupo(self, grupo: 'Grupo') -> None:
        if grupo in self.__grupos:
            self.__grupos.remove(grupo)

    def obtenerGrupos(self) -> List['Grupo']:
        return self.__grupos.copy()