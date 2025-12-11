from datetime import datetime
from typing import Optional


class PeriodoAcademico:
    def __init__(self, id_periodo: int, nombre_periodo: str, fecha_inicio: datetime, 
                 fecha_fin: datetime, actual: bool = False):
        self.__id_periodo = id_periodo
        self.__nombre_periodo = nombre_periodo
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__actual = actual

    @property
    def id_periodo(self) -> int:
        return self.__id_periodo

    @property
    def nombre_periodo(self) -> str:
        return self.__nombre_periodo

    @property
    def fecha_inicio(self) -> datetime:
        return self.__fecha_inicio

    @property
    def fecha_fin(self) -> datetime:
        return self.__fecha_fin

    @property
    def actual(self) -> bool:
        return self.__actual

    @actual.setter
    def actual(self, value: bool) -> None:
        self.__actual = value

    def es_actual(self) -> bool:
        return self.__actual
