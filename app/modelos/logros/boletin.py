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
        self.id_boletin = id_boletin
        self.id_estudiante = id_estudiante
        self.id_periodo = id_periodo
        self.id_generador = id_generador
        self.fecha_generacion = fecha_generacion
        self.calificaciones: List['EvaluacionLogro'] = []
    @property
    def calificaciones(self) -> List['EvaluacionLogro']:
        return self.calificaciones.copy()
