from datetime import datetime

class Notificacion:
    def __init__(self, idNotificacion: int = None, destinatario: str = None, asunto: str = None,
                 contenido: str = None, leida: bool = False, fechaEnvio: datetime = None):
        self.__idNotificacion: int = idNotificacion
        self.__destinatario: str = destinatario
        self.__asunto: str = asunto
        self.__contenido: str = contenido
        self.__leida: bool = leida
        self.__fechaEnvio: datetime = fechaEnvio

    @property
    def idNotificacion(self) -> int:
        return self.__idNotificacion

    @property
    def destinatario(self) -> str:
        return self.__destinatario

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def contenido(self) -> str:
        return self.__contenido

    @property
    def leida(self) -> bool:
        return self.__leida

    def marcarLeida(self) -> None:
        self.__leida = True

    def resumen(self) -> str:
        return f"Notificación para {self.__destinatario}: {self.__asunto}"