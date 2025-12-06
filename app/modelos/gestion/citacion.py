from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .notificacion import Notificacion
    from ..usuarios.directivo import Directivo

class Citacion:
    def __init__(self, idCitacion: int, fechaProgramada: datetime, correoDestinatarios: List[str],
                 motivo: str, descripcion: str, lugar: str, remitente: 'Directivo'):
        self.__idCitacion: int = idCitacion
        self.__fechaProgramada: datetime = fechaProgramada
        self.__correoDestinatarios: List[str] = correoDestinatarios
        self.__motivo: str = motivo
        self.__descripcion: str = descripcion
        self.__lugar: str = lugar
        self.__remitente: 'Directivo' = remitente
        self.__notificacion: List['Notificacion'] = []

    @property
    def idCitacion(self) -> int:
        return self.__idCitacion

    @property
    def fechaProgramada(self) -> datetime:
        return self.__fechaProgramada

    @property
    def correoDestinatarios(self) -> List[str]:
        return self.__correoDestinatarios.copy()

    @property
    def motivo(self) -> str:
        return self.__motivo

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def lugar(self) -> str:
        return self.__lugar

    @property
    def remitente(self) -> 'Directivo':
        return self.__remitente

    @property
    def notificacion(self) -> List['Notificacion']:
        return self.__notificacion.copy()

    def agregarDestinatarios(self, correo: str) -> None:
        if correo not in self.__correoDestinatarios:
            self.__correoDestinatarios.append(correo)

    def eliminarDestinatarios(self, correo: str) -> None:
        if correo in self.__correoDestinatarios:
            self.__correoDestinatarios.remove(correo)

    def agregarNotificacion(self, notificacion: 'Notificacion') -> None:
        if notificacion not in self.__notificacion:
            self.__notificacion.append(notificacion)

    def eliminarNotificacion(self, notificacion: 'Notificacion') -> None:
        if notificacion in self.__notificacion:
            self.__notificacion.remove(notificacion)