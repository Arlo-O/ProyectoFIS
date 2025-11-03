from datetime import datetime

class Anotacion:
    def __init__(self, idAnotacion: int = None, autor: str = None, contenido: str = None, fecha: datetime = None):
        self.__idAnotacion: int = idAnotacion
        self.__autor: str = autor
        self.__contenido: str = contenido
        self.__fecha: datetime = fecha

    @property
    def idAnotacion(self) -> int:
        return self.__idAnotacion

    @property
    def autor(self) -> str:
        return self.__autor

    @property
    def contenido(self) -> str:
        return self.__contenido

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    def resumen(self) -> str:
        return f"{self.__fecha}: {self.__autor} - {self.__contenido[:50]}"