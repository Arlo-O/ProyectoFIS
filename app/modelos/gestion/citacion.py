from datetime import datetime
from typing import List, TYPE_CHECKING
from typing import Optional


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from .notificacion import Notificacion


class Citacion:
    def __init__(self, id_citacion: int, fecha_programada: datetime, motivo: str, 
                 descripcion: str, lugar: str, id_remitente: Optional[int] = None,
                 id_entrevista: Optional[int] = None):
        self.__id_citacion = id_citacion
        self.__fecha_programada = fecha_programada
        self.__correo_destinatarios: List[str] = []
        self.__motivo = motivo
        self.__descripcion = descripcion
        self.__lugar = lugar
        self.__id_remitente = id_remitente
        self.__id_entrevista = id_entrevista
        self.__notificaciones: List['Notificacion'] = []

    @property
    def id_citacion(self) -> int:
        return self.__id_citacion

    @property
    def fecha_programada(self) -> datetime:
        return self.__fecha_programada

    @property
    def correo_destinatarios(self) -> List[str]:
        return self.__correo_destinatarios.copy()

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
    def id_remitente(self) -> Optional[int]:
        return self.__id_remitente

    @property
    def id_entrevista(self) -> Optional[int]:
        return self.__id_entrevista

    @property
    def notificaciones(self) -> List['Notificacion']:
        return self.__notificaciones.copy()

    def agregar_destinatario(self, correo: str) -> None:
        if correo not in self.__correo_destinatarios:
            self.__correo_destinatarios.append(correo)

    def eliminar_destinatario(self, correo: str) -> None:
        if correo in self.__correo_destinatarios:
            self.__correo_destinatarios.remove(correo)

    def agregar_notificacion(self, notificacion: 'Notificacion') -> None:
        if notificacion not in self.__notificaciones:
            self.__notificaciones.append(notificacion)
