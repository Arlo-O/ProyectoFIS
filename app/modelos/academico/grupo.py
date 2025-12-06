from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..usuarios.profesor import Profesor
    from ..usuarios.directivo import Directivo
    from ..interfaces.igeneradorPDF import IGeneradorPDF

class Grupo:
    def __init__(self, idGrupo: int, nombreGrupo: str, directorGrupo: 'Profesor', 
                 creador: 'Directivo', cupoMaximo: int = 10, cupoMinimo: int = 5, activo: bool = True):
        self.__idGrupo: int = idGrupo
        self.__nombreGrupo: str = nombreGrupo
        self.__directorGrupo: 'Profesor' = directorGrupo
        self.__creador: 'Directivo' = creador
        self.__cupoMaximo: int = cupoMaximo
        self.__cupoMinimo: int = cupoMinimo
        self.__activo: bool = activo
        self.__estudiantes: List['Estudiante'] = []

    @property
    def idGrupo(self) -> int:
        return self.__idGrupo

    @property
    def nombreGrupo(self) -> str:
        return self.__nombreGrupo

    @property
    def directorGrupo(self) -> 'Profesor':
        return self.__directorGrupo

    @property
    def creador(self) -> 'Directivo':
        return self.__creador

    @property
    def numEstudiantes(self) -> int:
        return len(self.__estudiantes)

    @property
    def cupoMaximo(self) -> int:
        return self.__cupoMaximo

    @cupoMaximo.setter
    def cupoMaximo(self, value: int) -> None:
        self.__cupoMaximo = value

    @property
    def cupoMinimo(self) -> int:
        return self.__cupoMinimo

    @property
    def activo(self) -> bool:
        return self.__activo

    @activo.setter
    def activo(self, value: bool) -> None:
        self.__activo = value

    def agregarEstudiante(self, estudiante: 'Estudiante') -> None:
        if self.cupoDisponible() and estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)

    def eliminarEstudiante(self, estudiante: 'Estudiante') -> None:
        if estudiante in self.__estudiantes:
            self.__estudiantes.remove(estudiante)

    def cupoDisponible(self) -> bool:
        return len(self.__estudiantes) < self.__cupoMaximo

    def obtenerEstudiantes(self) -> List['Estudiante']:
        return self.__estudiantes.copy()

    def generarListadoPDF(self, generador: 'IGeneracionPDF') -> str:
        # Logic to generate PDF
        return "PDF Content"