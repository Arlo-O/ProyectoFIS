from datetime import datetime
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..academico.periodoAcademico import PeriodoAcademico
    from ..usuarios.profesor import Profesor
    from .evaluacionLogro import EvaluacionLogro


class Boletin:
    def __init__(self, id_boletin: int, id_estudiante: int, id_periodo: int, 
                 id_generador: Optional[int], fecha_generacion: datetime):
        self.__id_boletin = id_boletin
        self.__id_estudiante = id_estudiante
        self.__id_periodo = id_periodo
        self.__id_generador = id_generador
        self.__fecha_generacion = fecha_generacion
        self.__calificaciones: List['EvaluacionLogro'] = []

    @property
    def id_boletin(self) -> int:
        return self.__id_boletin

    @property
    def id_estudiante(self) -> int:
        return self.__id_estudiante

    @property
    def id_periodo(self) -> int:
        return self.__id_periodo

    @property
    def id_generador(self) -> Optional[int]:
        return self.__id_generador

    @property
    def fecha_generacion(self) -> datetime:
        return self.__fecha_generacion

    @property
    def calificaciones(self) -> List['EvaluacionLogro']:
        return self.__calificaciones.copy()
