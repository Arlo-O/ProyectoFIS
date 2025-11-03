class Grado:
    def __init__(self, idGrado: int = None, nombre: str = None, nivel: str = None):
        self.__idGrado: int = idGrado
        self.__nombre: str = nombre
        self.__nivel: str = nivel

    @property
    def idGrado(self) -> int:
        return self.__idGrado

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def nivel(self) -> str:
        return self.__nivel

    def descripcion(self) -> str:
        return f"{self.__nombre} ({self.__nivel})"