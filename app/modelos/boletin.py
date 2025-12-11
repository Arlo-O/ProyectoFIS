class Boletin:
    def __init__(self, idBoletin: int = None, estudiante = None, periodo: str = None, calificaciones: dict = None):
        self.__idBoletin: int = idBoletin
        self.__estudiante = estudiante
        self.__periodo: str = periodo
        self.__calificaciones: dict = calificaciones or {}

    @property
    def idBoletin(self) -> int:
        return self.__idBoletin

    @property
    def estudiante(self):
        return self.__estudiante

    @property
    def periodo(self) -> str:
        return self.__periodo

    @property
    def calificaciones(self) -> dict:
        return self.__calificaciones.copy()

    def agregarCalificacion(self, materia: str, nota: float) -> None:
        self.__calificaciones[materia] = nota

    def promedio(self) -> float:
        if not self.__calificaciones:
            return 0.0
        return sum(self.__calificaciones.values()) / len(self.__calificaciones)

    def resumen(self) -> str:
        nombreEstudiante = self.__estudiante.primerNombre if self.__estudiante else "Desconocido"
        return f"Boletín {self.__idBoletin} - Estudiante {nombreEstudiante} - Promedio {self.promedio():.2f}"