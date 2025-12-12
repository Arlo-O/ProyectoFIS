from datetime import datetime
from typing import Optional


class PeriodoAcademico:
    def __init__(self, id_periodo: int, nombre_periodo: str, fecha_inicio: datetime, 
                 fecha_fin: datetime, actual: bool = False):
        self.id_periodo = id_periodo
        self.nombre_periodo = nombre_periodo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.actual = actual

    def es_actual(self) -> bool:
        return self.actual
