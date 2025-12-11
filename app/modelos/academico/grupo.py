from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..usuarios.profesor import Profesor
    from ..usuarios.directivo import Directivo


class Grupo:
    def __init__(self, id_grupo: int, nombre_grupo: str, cupo_maximo: int = 10, 
                 cupo_minimo: int = 5, activo: bool = True, id_director: int = None, 
                 id_creador: int = None, id_grado: int = None):
        self.__id_grupo = id_grupo
        self.__nombre_grupo = nombre_grupo
        self.__cupo_maximo = cupo_maximo
        self.__cupo_minimo = cupo_minimo
        self.__activo = activo
        self.__id_director = id_director
        self.__id_creador = id_creador
        self.__id_grado = id_grado
        self.__estudiantes: List['Estudiante'] = []

    @property
    def id_grupo(self) -> int:
        return self.__id_grupo

    @property
    def nombre_grupo(self) -> str:
        return self.__nombre_grupo

    @property
    def cupo_maximo(self) -> int:
        return self.__cupo_maximo

    @cupo_maximo.setter
    def cupo_maximo(self, value: int) -> None:
        self.__cupo_maximo = value

    @property
    def cupo_minimo(self) -> int:
        return self.__cupo_minimo

    @property
    def activo(self) -> bool:
        return self.__activo

    @activo.setter
    def activo(self, value: bool) -> None:
        self.__activo = value

    @property
    def id_director(self) -> int:
        return self.__id_director

    @property
    def id_creador(self) -> int:
        return self.__id_creador

    @property
    def id_grado(self) -> int:
        return self.__id_grado

    @property
    def num_estudiantes(self) -> int:
        return len(self.__estudiantes)

    @property
    def estudiantes(self) -> List['Estudiante']:
        return self.__estudiantes.copy()

    def agregar_estudiante(self, estudiante: 'Estudiante') -> bool:
        if self.cupo_disponible() and estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)
            return True
        return False

    def eliminar_estudiante(self, estudiante: 'Estudiante') -> bool:
        if estudiante in self.__estudiantes:
            self.__estudiantes.remove(estudiante)
            return True
        return False

    def cupo_disponible(self) -> bool:
        return len(self.__estudiantes) < self.__cupo_maximo
