from typing import List, TYPE_CHECKING
from .usuario import Usuario


if TYPE_CHECKING:
    from .persona import Persona
    from .estudiante import Estudiante


class Acudiente(Usuario):
    def __init__(self, id_acudiente: int, parentesco: str = "", es_aspirante: bool = False):
        super().__init__()
        self.__id_acudiente = id_acudiente
        self.__parentesco = parentesco
        self.__es_aspirante = es_aspirante
        self.__estudiantes: List['Estudiante'] = []

    @property
    def id_acudiente(self) -> int:
        return self.__id_acudiente

    @property
    def parentesco(self) -> str:
        return self.__parentesco

    @parentesco.setter
    def parentesco(self, value: str) -> None:
        self.__parentesco = value

    @property
    def es_aspirante(self) -> bool:
        return self.__es_aspirante

    @es_aspirante.setter
    def es_aspirante(self, value: bool) -> None:
        self.__es_aspirante = value

    @property
    def estudiantes(self) -> List['Estudiante']:
        return self.__estudiantes.copy()
