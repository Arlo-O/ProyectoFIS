from datetime import datetime
from typing import Dict, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.aspirante import Aspirante


class RespuestaFormPre:
    def __init__(self, id_respuesta: int, id_aspirante: Optional[int], 
                 fecha_respuesta: datetime, respuestas: Dict[str, str]):
        self.id_respuesta = id_respuesta
        self.id_aspirante = id_aspirante
        self.fecha_respuesta = fecha_respuesta
        self.respuestas = respuestas
    @property
    def respuestas(self) -> Dict[str, str]:
        return self.respuestas.copy()
