from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..logros.logro import Logro
    from .grupo import Grupo

class HojaVidaAcademica:
    def __init__(self, idHojaVida: int, estudiante: 'Estudiante', promedioGeneral: float = 0.0):
        self.__idHojaVida: int = idHojaVida
        self.__estudiante: 'Estudiante' = estudiante
        self.__promedioGeneral: float = promedioGeneral
        self.__logrosDestacados: List['Logro'] = []
        self.__historialGrupos: List['Grupo'] = []

    @property
    def idHojaVida(self) -> int:
        return self.__idHojaVida

    @property
    def estudiante(self) -> 'Estudiante':
        return self.__estudiante

    @property
    def promedioGeneral(self) -> float:
        return self.__promedioGeneral

    @property
    def logrosDestacados(self) -> List['Logro']:
        return self.__logrosDestacados.copy()

    @property
    def historialGrupos(self) -> List['Grupo']:
        return self.__historialGrupos.copy()

    def actualizarPromedio(self, nuevoPromedio: float) -> None:
        self.__promedioGeneral = nuevoPromedio

    def agregarLogroDestacado(self, logro: 'Logro') -> None:
        if logro not in self.__logrosDestacados:
            self.__logrosDestacados.append(logro)