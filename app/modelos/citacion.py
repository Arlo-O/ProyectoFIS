from datetime import datetime

class Citacion:
    def __init__(self, idCitacion: int = None, fecha: datetime = None, motivo: str = None,
                 estado: str = None, remitente: str = None, destinatario: str = None):
        self.__idCitacion: int = idCitacion
        self.__fecha: datetime = fecha
        self.__motivo: str = motivo
        self.__estado: str = estado
        self.__remitente: str = remitente
        self.__destinatario: str = destinatario

    @property
    def idCitacion(self) -> int:
        return self.__idCitacion

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @property
    def motivo(self) -> str:
        return self.__motivo

    @property
    def estado(self) -> str:
        return self.__estado

    def cambiarEstado(self, nuevoEstado: str) -> None:
        self.__estado = nuevoEstado

    def resumen(self) -> str:
        return f"Citación {self.__idCitacion}: {self.__motivo} - {self.__estado}"