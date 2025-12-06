from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.acudiente import Acudiente
    from .iEnvioCorreo import IEnvioCorreo

class Notificacion:
    def __init__(self, idNotificacion: int, fechaEnvio: datetime, asunto: str, 
                 contenido: str, destinatario: 'Acudiente'):
        self.__idNotificacion: int = idNotificacion
        self.__fechaEnvio: datetime = fechaEnvio
        self.__asunto: str = asunto
        self.__contenido: str = contenido
        self.__destinatario: 'Acudiente' = destinatario

    @property
    def idNotificacion(self) -> int:
        return self.__idNotificacion

    @property
    def fechaEnvio(self) -> datetime:
        return self.__fechaEnvio

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def contenido(self) -> str:
        return self.__contenido

    @property
    def destinatario(self) -> 'Acudiente':
        return self.__destinatario

    def enviar(self, envioCorreo: 'IEnvioCorreo') -> None:
        # Logic to send email
        pass