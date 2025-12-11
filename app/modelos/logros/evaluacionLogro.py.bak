from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .logro import Logro
    from ..usuarios.profesor import Profesor
    from ..academico.periodoAcademico import PeriodoAcademico
    from ..usuarios.estudiante import Estudiante
    from ..logros.boletin import Boletin


class EvaluacionLogro:
    def __init__(self, id_evaluacion: int, id_logro: int, id_profesor: int, 
                 id_periodo: int, puntuacion: str, fecha_registro: datetime,
                 comentarios: dict = None, id_estudiante: Optional[int] = None,
                 id_boletin: Optional[int] = None):
        self.__id_evaluacion = id_evaluacion
        self.__id_logro = id_logro
        self.__id_profesor = id_profesor
        self.__id_periodo = id_periodo
        self.__puntuacion = puntuacion
        self.__fecha_registro = fecha_registro
        self.__comentarios = comentarios or {}
        self.__id_estudiante = id_estudiante
        self.__id_boletin = id_boletin

    @property
    def id_evaluacion(self) -> int:
        return self.__id_evaluacion

    @property
    def id_logro(self) -> int:
        return self.__id_logro

    @property
    def id_profesor(self) -> int:
        return self.__id_profesor

    @property
    def id_periodo(self) -> int:
        return self.__id_periodo

    @property
    def puntuacion(self) -> str:
        return self.__puntuacion

    @puntuacion.setter
    def puntuacion(self, value: str) -> None:
        self.__puntuacion = value

    @property
    def fecha_registro(self) -> datetime:
        return self.__fecha_registro

    @property
    def comentarios(self) -> dict:
        return self.__comentarios.copy()

    @property
    def id_estudiante(self) -> Optional[int]:
        return self.__id_estudiante

    @property
    def id_boletin(self) -> Optional[int]:
        return self.__id_boletin
