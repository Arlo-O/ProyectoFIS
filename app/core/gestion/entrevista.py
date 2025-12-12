from datetime import datetime
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor
    from ..usuarios.directivo import Directivo
    from ..usuarios.aspirante import Aspirante
    from .citacion import Citacion


class Entrevista:
    def __init__(self, id_entrevista: int, notas: str, fecha_programada: datetime, 
                 lugar: str, estado: str, id_entrevistador: Optional[int] = None,
                 id_remitente: Optional[int] = None, id_aspirante: Optional[int] = None):
        self.id_entrevista = id_entrevista
        self.notas = notas
        self.fecha_programada = fecha_programada
        self.lugar = lugar
        self.estado = estado
        self.id_entrevistador = id_entrevistador
        self.id_remitente = id_remitente
        self.id_aspirante = id_aspirante
        self.citaciones: List['Citacion'] = []
    @property
    def citaciones(self) -> List['Citacion']:
        return self.citaciones.copy()
