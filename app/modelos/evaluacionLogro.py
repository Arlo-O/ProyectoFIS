from datetime import datetime

class EvaluacionLogro:
    def __init__(self, idEvaluacion: int = None, idLogro: int = None, idEvaluador: int = None,
                 fecha: datetime = None, puntuacion: float = None, comentarios: str = None):
        self.__idEvaluacion: int = idEvaluacion
        self.__idLogro: int = idLogro
        self.__idEvaluador: int = idEvaluador
        self.__fecha: datetime = fecha
        self.__puntuacion: float = puntuacion
        self.__comentarios: str = comentarios

    @property
    def idEvaluacion(self) -> int:
        return self.__idEvaluacion

    @property
    def idLogro(self) -> int:
        return self.__idLogro

    @property
    def idEvaluador(self) -> int:
        return self.__idEvaluador

    @property
    def fecha(self):
        return self.__fecha

    @property
    def puntuacion(self) -> float:
        return self.__puntuacion

    def asignarPuntuacion(self, puntuacion: float) -> None:
        self.__puntuacion = puntuacion

    def agregarComentario(self, comentario: str) -> None:
        self.__comentarios = (self.__comentarios or "") + "\n" + comentario if comentario else self.__comentarios

    def resumen(self) -> str:
        return f"Evaluación {self.__idEvaluacion} - Logro {self.__idLogro} - Puntuación {self.__puntuacion}"