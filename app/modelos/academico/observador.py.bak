from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from .anotacion import Anotacion


class Observador:
    def __init__(self, id_observador: int, id_estudiante: int, comportamiento_general: str = ""):
        self.__id_observador = id_observador
        self.__id_estudiante = id_estudiante
        self.__comportamiento_general = comportamiento_general
        self.__anotaciones: List['Anotacion'] = []

    @property
    def id_observador(self) -> int:
        return self.__id_observador

    @property
    def id_estudiante(self) -> int:
        return self.__id_estudiante

    @property
    def comportamiento_general(self) -> str:
        return self.__comportamiento_general

    @comportamiento_general.setter
    def comportamiento_general(self, value: str) -> None:
        self.__comportamiento_general = value

    @property
    def anotaciones(self) -> List['Anotacion']:
        return self.__anotaciones.copy()

    def agregar_anotacion(self, anotacion: 'Anotacion') -> None:
        if anotacion not in self.__anotaciones:
            self.__anotaciones.append(anotacion)
