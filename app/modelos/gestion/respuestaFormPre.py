from datetime import datetime
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..usuarios.aspirante import Aspirante

class RespuestaFormPre:
    def __init__(self, idRespuesta: int, aspirante: 'Aspirante', fechaRespuesta: datetime, 
                 respuestas: Dict[str, str]):
        self.__idRespuesta: int = idRespuesta
        self.__aspirante: 'Aspirante' = aspirante
        self.__fechaRespuesta: datetime = fechaRespuesta
        self.__respuestas: Dict[str, str] = respuestas

    @property
    def idRespuesta(self) -> int:
        return self.__idRespuesta

    @property
    def aspirante(self) -> 'Aspirante':
        return self.__aspirante

    @property
    def fechaRespuesta(self) -> datetime:
        return self.__fechaRespuesta

    @property
    def respuestas(self) -> Dict[str, str]:
        return self.__respuestas.copy()