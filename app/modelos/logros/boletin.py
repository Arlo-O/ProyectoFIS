from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..academico.periodoAcademico import PeriodoAcademico
    from ..usuarios.profesor import Profesor
    from .evaluacionLogro import EvaluacionLogro
    from ..interfaces.igeneradorPDF import IGeneradorPDF

class Boletin:
    def __init__(self, idBoletin: int, estudiante: 'Estudiante', periodo: 'PeriodoAcademico', 
                 generadoPor: 'Profesor', fechaGeneracion: datetime):
        self.__idBoletin: int = idBoletin
        self.__estudiante: 'Estudiante' = estudiante
        self.__periodo: 'PeriodoAcademico' = periodo
        self.__generadoPor: 'Profesor' = generadoPor
        self.__fechaGeneracion: datetime = fechaGeneracion
        self.__calificaciones: List['EvaluacionLogro'] = []

    @property
    def idBoletin(self) -> int:
        return self.__idBoletin

    @property
    def estudiante(self) -> 'Estudiante':
        return self.__estudiante

    @property
    def periodo(self) -> 'PeriodoAcademico':
        return self.__periodo

    @property
    def generadoPor(self) -> 'Profesor':
        return self.__generadoPor

    @property
    def fechaGeneracion(self) -> datetime:
        return self.__fechaGeneracion

    @property
    def calificaciones(self) -> List['EvaluacionLogro']:
        return self.__calificaciones.copy()

    def agregarCalificacion(self, evaluacion: 'EvaluacionLogro') -> None:
        if evaluacion not in self.__calificaciones:
            self.__calificaciones.append(evaluacion)

    def eliminarCalificacion(self, evaluacion: 'EvaluacionLogro') -> None:
        if evaluacion in self.__calificaciones:
            self.__calificaciones.remove(evaluacion)

    def obtenerEvaluaciones(self) -> List['EvaluacionLogro']:
        return self.__calificaciones.copy()

    def generarPDF(self, generador: 'IGeneracionPDF') -> str:
        # Logic to generate PDF
        return "PDF Content"