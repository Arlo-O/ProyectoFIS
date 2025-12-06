from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .logro import Logro
    from ..usuarios.profesor import Profesor
    from ..academico.periodoAcademico import PeriodoAcademico

class EvaluacionLogro:
    def __init__(self, idEvaluacion: int, logro: 'Logro', profesor: 'Profesor', 
                 periodo: 'PeriodoAcademico', puntuacion: str, fechaRegistro: datetime, 
                 comentarios: List[str] = None):
        self.__idEvaluacion: int = idEvaluacion
        self.__logro: 'Logro' = logro
        self.__profesor: 'Profesor' = profesor
        self.__periodo: 'PeriodoAcademico' = periodo
        self.__puntuacion: str = puntuacion
        self.__fechaRegistro: datetime = fechaRegistro
        self.__comentarios: List[str] = comentarios or []

    @property
    def idEvaluacion(self) -> int:
        return self.__idEvaluacion

    @property
    def logro(self) -> 'Logro':
        return self.__logro

    @property
    def profesor(self) -> 'Profesor':
        return self.__profesor

    @property
    def periodo(self) -> 'PeriodoAcademico':
        return self.__periodo

    @property
    def puntuacion(self) -> str:
        return self.__puntuacion

    @property
    def fechaRegistro(self) -> datetime:
        return self.__fechaRegistro

    @property
    def comentarios(self) -> List[str]:
        return self.__comentarios.copy()

    @puntuacion.setter
    def puntuacion(self, nuevaPuntuacion: str) -> None:
        self.__puntuacion = nuevaPuntuacion

    def agregarComentario(self, comentario: str) -> None:
        self.__comentarios.append(comentario)