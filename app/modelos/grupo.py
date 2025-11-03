class Grupo:
    def __init__(self, idGrupo: int = None, nombre: str = None, grado: str = None, anio: int = None):
        self.__idGrupo: int = idGrupo
        self.__nombre: str = nombre
        self.__grado: str = grado
        self.__anio: int = anio
        self.__estudiantes: list = []
        self.__profesores: list = []

    @property
    def idGrupo(self) -> int:
        return self.__idGrupo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def grado(self) -> str:
        return self.__grado

    @property
    def anio(self) -> int:
        return self.__anio

    def agregarEstudiante(self, estudiante) -> None:
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)

    def removerEstudiante(self, estudiante) -> None:
        try:
            self.__estudiantes.remove(estudiante)
        except ValueError:
            pass

    def asignarProfesor(self, profesor) -> None:
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)

    def obtenerEstudiantes(self) -> list:
        return self.__estudiantes.copy()

    def obtenerProfesores(self) -> list:
        return self.__profesores.copy()