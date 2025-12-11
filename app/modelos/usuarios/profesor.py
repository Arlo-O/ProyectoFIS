from typing import List, TYPE_CHECKING
from .usuario import Usuario


if TYPE_CHECKING:
    from ..academico.grupo import Grupo


class Profesor(Usuario):
    def __init__(self, id_profesor: int, es_director_grupo: bool = False):
        super().__init__()
        self.__id_profesor = id_profesor
        self.__es_director_grupo = es_director_grupo
        self.__grupos_asignados: List['Grupo'] = []

    @property
    def id_profesor(self) -> int:
        return self.__id_profesor

    @property
    def es_director_grupo(self) -> bool:
        return self.__es_director_grupo

    @es_director_grupo.setter
    def es_director_grupo(self, value: bool) -> None:
        self.__es_director_grupo = value

    @property
    def grupos_asignados(self) -> List['Grupo']:
        return self.__grupos_asignados.copy()
