from datetime import datetime

class Logro:
    def __init__(self, idLogro: int = None, descripcion: str = None, fechaCreacion: datetime = None,
                 fechaLimite: datetime = None, estado: str = None):
        self.__idLogro: int = idLogro
        self.__descripcion: str = descripcion
        self.__fechaCreacion: datetime = fechaCreacion
        self.__fechaLimite: datetime = fechaLimite
        self.__estado: str = estado

    @property
    def idLogro(self) -> int:
        return self.__idLogro

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def fechaCreacion(self) -> datetime:
        return self.__fechaCreacion

    @property
    def fechaLimite(self) -> datetime:
        return self.__fechaLimite

    @property
    def estado(self) -> str:
        return self.__estado

    @descripcion.setter
    def descripcion(self, nuevaDescripcion: str) -> None:
        self.__descripcion = nuevaDescripcion

    @estado.setter
    def estado(self, nuevoEstado: str) -> None:
        self.__estado = nuevoEstado

    def estaVencido(self) -> bool:
        if self.__fechaLimite is None:
            return False
        from datetime import datetime
        return datetime.now() > self.__fechaLimite

    def resumen(self) -> str:
        return f"{self.__descripcion} ({self.__estado})"