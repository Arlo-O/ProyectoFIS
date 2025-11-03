class HojaVidaAcademica:
    def __init__(self, idHoja: int = None, idEstudiante: int = None, registros: list = None):
        self.__idHoja: int = idHoja
        self.__idEstudiante: int = idEstudiante
        self.__registros: list = registros or []

    @property
    def idHoja(self) -> int:
        return self.__idHoja

    @property
    def idEstudiante(self) -> int:
        return self.__idEstudiante

    def agregarRegistro(self, registro) -> None:
        self.__registros.append(registro)

    def obtenerRegistros(self) -> list:
        return self.__registros.copy()

    def resumen(self) -> str:
        return f"Hoja de vida académico {self.__idHoja} - Estudiante {self.__idEstudiante} - {len(self.__registros)} registros"