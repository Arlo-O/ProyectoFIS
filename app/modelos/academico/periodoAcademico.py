from datetime import datetime

class PeriodoAcademico:
    def __init__(self, idPeriodo: int, nombrePeriodo: str, fechaInicio: datetime, 
                 fechaFin: datetime, actual: bool = False):
        self.__idPeriodo: int = idPeriodo
        self.__nombrePeriodo: str = nombrePeriodo
        self.__fechaInicio: datetime = fechaInicio
        self.__fechaFin: datetime = fechaFin
        self.__actual: bool = actual

    @property
    def idPeriodo(self) -> int:
        return self.__idPeriodo

    @property
    def nombrePeriodo(self) -> str:
        return self.__nombrePeriodo

    @property
    def fechaInicio(self) -> datetime:
        return self.__fechaInicio

    @property
    def fechaFin(self) -> datetime:
        return self.__fechaFin

    @property
    def actual(self) -> bool:
        return self.__actual

    @actual.setter
    def actual(self, valor: bool) -> None:
        self.__actual = valor

    def esActual(self) -> bool:
        return self.__actual

    def cerrarPeriodo(self) -> None:
        self.__actual = False

    def abrirPeriodo(self, nombre: str, fechaInicio: datetime, fechaFin: datetime) -> None:
        # Logic to create/open new period (might be static or factory, but dictionary puts it here)
        # Assuming it updates current instance or similar
        self.__nombrePeriodo = nombre
        self.__fechaInicio = fechaInicio
        self.__fechaFin = fechaFin
        self.__actual = True