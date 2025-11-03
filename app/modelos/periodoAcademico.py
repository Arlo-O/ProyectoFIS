from datetime import datetime

class PeriodoAcademico:
    def __init__(self, idPeriodo: int = None, nombre: str = None, fechaInicio: datetime = None, fechaFin: datetime = None, activo: bool = True):
        self.__idPeriodo: int = idPeriodo
        self.__nombre: str = nombre
        self.__fechaInicio: datetime = fechaInicio
        self.__fechaFin: datetime = fechaFin
        self.__activo: bool = activo

    @property
    def idPeriodo(self) -> int:
        return self.__idPeriodo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def fechaInicio(self) -> datetime:
        return self.__fechaInicio

    @property
    def fechaFin(self) -> datetime:
        return self.__fechaFin

    @property
    def activo(self) -> bool:
        return self.__activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        self.__activo = valor

    def estaActivo(self) -> bool:
        return self.__activo and (self.__fechaFin is None or datetime.now() <= self.__fechaFin)

    def duracionDias(self) -> int:
        if self.__fechaInicio and self.__fechaFin:
            return (self.__fechaFin - self.__fechaInicio).days
        return 0