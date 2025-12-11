from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..logros.logro import Logro
    from .grupo import Grupo


class HojaVidaAcademica:
    def __init__(self, id_hoja_vida: int, id_estudiante: int, promedio_general: float = 0.0):
        self.__id_hoja_vida = id_hoja_vida
        self.__id_estudiante = id_estudiante
        self.__promedio_general = promedio_general
        self.__logros_destacados: List['Logro'] = []
        self.__historial_grupos: List['Grupo'] = []

    @property
    def id_hoja_vida(self) -> int:
        return self.__id_hoja_vida

    @property
    def id_estudiante(self) -> int:
        return self.__id_estudiante

    @property
    def promedio_general(self) -> float:
        return self.__promedio_general

    @promedio_general.setter
    def promedio_general(self, value: float) -> None:
        self.__promedio_general = value

    @property
    def logros_destacados(self) -> List['Logro']:
        return self.__logros_destacados.copy()

    @property
    def historial_grupos(self) -> List['Grupo']:
        return self.__historial_grupos.copy()

    def agregar_logro_destacado(self, logro: 'Logro') -> None:
        if logro not in self.__logros_destacados:
            self.__logros_destacados.append(logro)

    def agregar_grupo_historial(self, grupo: 'Grupo') -> None:
        if grupo not in self.__historial_grupos:
            self.__historial_grupos.append(grupo)
