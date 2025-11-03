class Evaluacion:
    def __init__(self, idEvaluacion: int = None, descripcion: str = None, peso: float = 0.0):
        self.__idEvaluacion: int = idEvaluacion
        self.__descripcion: str = descripcion
        self.__peso: float = peso

    @property
    def idEvaluacion(self) -> int:
        return self.__idEvaluacion

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def peso(self) -> float:
        return self.__peso

    def actualizarPeso(self, nuevoPeso: float) -> None:
        self.__peso = nuevoPeso

    def __str__(self) -> str:
        return f"Evaluacion {self.__idEvaluacion}: {self.__descripcion} (peso={self.__peso})"