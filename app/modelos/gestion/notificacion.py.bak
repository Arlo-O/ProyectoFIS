from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.acudiente import Acudiente


class Notificacion:
    def __init__(self, id_notificacion: int, fecha_envio: datetime, asunto: str, 
                 contenido: str, id_destinatario: Optional[int] = None, 
                 id_citacion: Optional[int] = None):
        self.__id_notificacion = id_notificacion
        self.__fecha_envio = fecha_envio
        self.__asunto = asunto
        self.__contenido = contenido
        self.__id_destinatario = id_destinatario
        self.__id_citacion = id_citacion

    @property
    def id_notificacion(self) -> int:
        return self.__id_notificacion

    @property
    def fecha_envio(self) -> datetime:
        return self.__fecha_envio

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def contenido(self) -> str:
        return self.__contenido

    @property
    def id_destinatario(self) -> Optional[int]:
        return self.__id_destinatario

    @property
    def id_citacion(self) -> Optional[int]:
        return self.__id_citacion
