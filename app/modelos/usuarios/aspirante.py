from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from .usuario import Usuario


if TYPE_CHECKING:
    from ..gestion.entrevista import Entrevista
    from .acudiente import Acudiente


class Aspirante(Usuario):
    def __init__(self, id_aspirante: int, grado_solicitado: str = "", 
                 fecha_solicitud: Optional[datetime] = None, estado_proceso: str = "Preinscrito"):
        super().__init__()
        self.__id_aspirante = id_aspirante
        self.__grado_solicitado = grado_solicitado
        self.__fecha_solicitud = fecha_solicitud
        self.__estado_proceso = estado_proceso
        self.__entrevista: Optional['Entrevista'] = None
        self.__acudientes: List['Acudiente'] = []

    @property
    def id_aspirante(self) -> int:
        return self.__id_aspirante

    @property
    def grado_solicitado(self) -> str:
        return self.__grado_solicitado

    @property
    def fecha_solicitud(self) -> Optional[datetime]:
        return self.__fecha_solicitud

    @property
    def estado_proceso(self) -> str:
        return self.__estado_proceso

    @estado_proceso.setter
    def estado_proceso(self, value: str) -> None:
        self.__estado_proceso = value

    @property
    def entrevista(self) -> Optional['Entrevista']:
        return self.__entrevista

    @entrevista.setter
    def entrevista(self, value: Optional['Entrevista']) -> None:
        self.__entrevista = value

    @property
    def acudientes(self) -> List['Acudiente']:
        return self.__acudientes.copy()
