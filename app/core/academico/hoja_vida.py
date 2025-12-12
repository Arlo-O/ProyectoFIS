from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from ..logros.logro import Logro
    from .grupo import Grupo


class HojaVidaAcademica:
    def __init__(self, id_hoja_vida: int, id_estudiante: int, promedio_general: float = 0.0):
        self.id_hoja_vida = id_hoja_vida
        self.id_estudiante = id_estudiante
        self.promedio_general = promedio_general
        self.logros_destacados: List['Logro'] = []
        self.historial_grupos: List['Grupo'] = []

    @property
    def logros_destacados(self) -> List['Logro']:
        return self.logros_destacados.copy()

    @property
    def historial_grupos(self) -> List['Grupo']:
        return self.historial_grupos.copy()

    def agregar_logro_destacado(self, logro: 'Logro') -> None:
        if logro not in self.logros_destacados:
            self.logros_destacados.append(logro)

    def agregar_grupo_historial(self, grupo: 'Grupo') -> None:
        if grupo not in self.historial_grupos:
            self.historial_grupos.append(grupo)
