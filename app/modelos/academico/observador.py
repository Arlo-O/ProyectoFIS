from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from .anotacion import Anotacion

class Observador:
    def __init__(self, idObservador: int, estudiante: 'Estudiante', comportamientoGeneral: str = ""):
        self.__idObservador: int = idObservador
        self.__estudiante: 'Estudiante' = estudiante
        self.__comportamientoGeneral: str = comportamientoGeneral
        self.__anotaciones: List['Anotacion'] = []

    @property
    def idObservador(self) -> int:
        return self.__idObservador

    @property
    def estudiante(self) -> 'Estudiante':
        return self.__estudiante

    @property
    def comportamientoGeneral(self) -> str:
        return self.__comportamientoGeneral

    @property
    def anotaciones(self) -> List['Anotacion']:
        return self.__anotaciones.copy()

    @comportamientoGeneral.setter
    def comportamientoGeneral(self, nuevoComportamiento: str) -> None:
        self.__comportamientoGeneral = nuevoComportamiento

    def agregarAnotacion(self, anotacion: 'Anotacion') -> None:
        if anotacion not in self.__anotaciones:
            self.__anotaciones.append(anotacion)

    def generarReporte(self) -> str:
        # Logic to generate report
        return f"Reporte Observador: {self.__comportamientoGeneral}"