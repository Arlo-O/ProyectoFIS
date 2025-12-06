from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor
    from .citacion import Citacion
    from ..usuarios.directivo import Directivo
    from ..usuarios.aspirante import Aspirante

class Entrevista:
    def __init__(self, idEntrevista: int, notas: str, entrevistador: 'Profesor', 
                 fechaProgramada: datetime, lugar: str, estado: str, remitente: 'Directivo'):
        self.__idEntrevista: int = idEntrevista
        self.__notas: str = notas
        self.__entrevistador: 'Profesor' = entrevistador
        self.__fechaProgramada: datetime = fechaProgramada
        self.__lugar: str = lugar
        self.__estado: str = estado
        self.__citacion: List['Citacion'] = []
        self.__remitente: 'Directivo' = remitente
        self.__aspirante: Optional['Aspirante'] = None

    @property
    def idEntrevista(self) -> int:
        return self.__idEntrevista

    @property
    def notas(self) -> str:
        return self.__notas

    @property
    def entrevistador(self) -> 'Profesor':
        return self.__entrevistador

    @property
    def fechaProgramada(self) -> datetime:
        return self.__fechaProgramada

    @property
    def lugar(self) -> str:
        return self.__lugar

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def remitente(self) -> 'Directivo':
        return self.__remitente

    @property
    def citacion(self) -> List['Citacion']:
        return self.__citacion.copy()

    @property
    def aspirante(self) -> Optional['Aspirante']:
        return self.__aspirante

    @aspirante.setter
    def aspirante(self, aspirante: 'Aspirante') -> None:
        self.__aspirante = aspirante

    def agregarCitacion(self, citacion: 'Citacion') -> None:
        if citacion not in self.__citacion:
            self.__citacion.append(citacion)

