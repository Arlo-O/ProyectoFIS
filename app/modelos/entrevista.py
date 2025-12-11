from datetime import datetime

class Entrevista:
    def __init__(self, idEntrevista: int = None, descripcion: str = None, fecha: datetime = None):
        self.__idEntrevista: int = idEntrevista
        self.__descripcion: str = descripcion
        self.__fecha: datetime = fecha
        self.__citaciones: list = []

    @property
    def idEntrevista(self) -> int:
        return self.__idEntrevista

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    @idEntrevista.setter
    def idEntrevista(self, nuevoId: int) -> None:
        self.__idEntrevista = nuevoId

    @descripcion.setter
    def descripcion(self, nuevoDescripcion: str) -> None:
        self.__descripcion = nuevoDescripcion

    @fecha.setter
    def fecha(self, nuevaFecha: datetime) -> None:
        self.__fecha = nuevaFecha

    def agregarCitacion(self, citacion) -> None:
        if citacion not in self.__citaciones:
            self.__citaciones.append(citacion)

    def removerCitacion(self, citacion) -> None:
        try:
            self.__citaciones.remove(citacion)
        except ValueError:
            pass

    def obtenerCitaciones(self) -> list:
        return self.__citaciones.copy()

    def resumen(self) -> str:
        cantidadCitaciones = len(self.__citaciones)
        return f"Entrevista {self.__idEntrevista} - {cantidadCitaciones} citaciones"
