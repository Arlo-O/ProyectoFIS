from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.acudiente import Acudiente


class Notificacion:
    def __init__(self, id_notificacion: int, fecha_envio: datetime, asunto: str, 
                 contenido: str, id_destinatario: Optional[int] = None, 
                 id_citacion: Optional[int] = None):
        self.id_notificacion = id_notificacion
        self.fecha_envio = fecha_envio
        self.asunto = asunto
        self.contenido = contenido
        self.id_destinatario = id_destinatario
        self.id_citacion = id_citacion
