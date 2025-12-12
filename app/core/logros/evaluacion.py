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
        self.id_evaluacion = id_evaluacion
        self.id_logro = id_logro
        self.id_profesor = id_profesor
        self.id_periodo = id_periodo
        self.puntuacion = puntuacion
        self.fecha_registro = fecha_registro
        self.comentarios = comentarios or {}
        self.id_estudiante = id_estudiante
        self.id_boletin = id_boletin

    @property
    def comentarios(self) -> dict:
        return self.comentarios.copy()
