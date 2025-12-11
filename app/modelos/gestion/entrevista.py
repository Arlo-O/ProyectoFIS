from datetime import datetime
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor
    from ..usuarios.directivo import Directivo
    from ..usuarios.aspirante import Aspirante
    from .citacion import Citacion


class Entrevista:
    def __init__(self, id_entrevista: int, notas: str, fecha_programada: datetime, 
                 lugar: str, estado: str, id_entrevistador: Optional[int] = None,
                 id_remitente: Optional[int] = None, id_aspirante: Optional[int] = None):
        self.__id_entrevista = id_entrevista
        self.__notas = notas
        self.__fecha_programada = fecha_programada
        self.__lugar = lugar
        self.__estado = estado
        self.__id_entrevistador = id_entrevistador
        self.__id_remitente = id_remitente
        self.__id_aspirante = id_aspirante
        self.__citaciones: List['Citacion'] = []

    @property
    def id_entrevista(self) -> int:
        return self.__id_entrevista

    @property
    def notas(self) -> str:
        return self.__notas

    @property
    def fecha_programada(self) -> datetime:
        return self.__fecha_programada

    @property
    def lugar(self) -> str:
        return self.__lugar

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def id_entrevistador(self) -> Optional[int]:
        return self.__id_entrevistador

    @property
    def id_remitente(self) -> Optional[int]:
        return self.__id_remitente

    @property
    def id_aspirante(self) -> Optional[int]:
        return self.__id_aspirante

    @property
    def citaciones(self) -> List['Citacion']:
        return self.__citaciones.copy()
