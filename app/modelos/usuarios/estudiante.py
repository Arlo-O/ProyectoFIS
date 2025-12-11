from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario


if TYPE_CHECKING:
    from .acudiente import Acudiente
    from ..academico.grupo import Grupo
    from ..academico.hojaVidaAcademica import HojaVidaAcademica
    from ..academico.observador import Observador
    from ..logros.evaluacionLogro import EvaluacionLogro
    from ..logros.boletin import Boletin


class Estudiante(Usuario):
    def __init__(self, id_estudiante: int, fecha_ingreso: Optional[datetime] = None, 
                 codigo_matricula: str = ""):
        super().__init__()
        self.__id_estudiante = id_estudiante
        self.__fecha_ingreso = fecha_ingreso
        self.__codigo_matricula = codigo_matricula
        self.__acudientes: List['Acudiente'] = []
        self.__grupo: Optional['Grupo'] = None
        self.__hoja_vida: Optional['HojaVidaAcademica'] = None
        self.__observador: Optional['Observador'] = None
        self.__evaluaciones_logro: List['EvaluacionLogro'] = []

    @property
    def id_estudiante(self) -> int:
        return self.__id_estudiante

    @property
    def fecha_ingreso(self) -> Optional[datetime]:
        return self.__fecha_ingreso

    @property
    def codigo_matricula(self) -> str:
        return self.__codigo_matricula

    @codigo_matricula.setter
    def codigo_matricula(self, value: str) -> None:
        self.__codigo_matricula = value

    @property
    def grupo(self) -> Optional['Grupo']:
        return self.__grupo

    @grupo.setter
    def grupo(self, value: Optional['Grupo']) -> None:
        self.__grupo = value

    @property
    def hoja_vida(self) -> Optional['HojaVidaAcademica']:
        return self.__hoja_vida

    @property
    def observador(self) -> Optional['Observador']:
        return self.__observador

    @property
    def acudientes(self) -> List['Acudiente']:
        return self.__acudientes.copy()

    @property
    def evaluaciones_logro(self) -> List['EvaluacionLogro']:
        return self.__evaluaciones_logro.copy()
