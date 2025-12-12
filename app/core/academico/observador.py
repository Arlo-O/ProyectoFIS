from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.estudiante import Estudiante
    from .anotacion import Anotacion


class Observador:
    def __init__(self, id_observador: int, id_estudiante: int, comportamiento_general: str = ""):
        self.id_observador = id_observador
        self.id_estudiante = id_estudiante
        self.comportamiento_general = comportamiento_general
        self.anotaciones: List['Anotacion'] = []

    @property
    def anotaciones(self) -> List['Anotacion']:
        return self.anotaciones.copy()

    def agregar_anotacion(self, anotacion: 'Anotacion') -> None:
        if anotacion not in self.anotaciones:
            self.anotaciones.append(anotacion)
