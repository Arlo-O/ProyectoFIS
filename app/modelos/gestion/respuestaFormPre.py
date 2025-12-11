from datetime import datetime
from typing import Dict, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.aspirante import Aspirante


class RespuestaFormPre:
    def __init__(self, id_respuesta: int, id_aspirante: Optional[int], 
                 fecha_respuesta: datetime, respuestas: Dict[str, str]):
        self.__id_respuesta = id_respuesta
        self.__id_aspirante = id_aspirante
        self.__fecha_respuesta = fecha_respuesta
        self.__respuestas = respuestas

    @property
    def id_respuesta(self) -> int:
        return self.__id_respuesta

    @property
    def id_aspirante(self) -> Optional[int]:
        return self.__id_aspirante

    @property
    def fecha_respuesta(self) -> datetime:
        return self.__fecha_respuesta

    @property
    def respuestas(self) -> Dict[str, str]:
        return self.__respuestas.copy()
