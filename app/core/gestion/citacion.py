from datetime import datetime
from typing import List, TYPE_CHECKING
from typing import Optional


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from .notificacion import Notificacion


class Citacion:
    def __init__(self, id_citacion: int, fecha_programada: datetime, motivo: str, 
                 descripcion: str, lugar: str, id_remitente: Optional[int] = None,
                 id_entrevista: Optional[int] = None):
        self.id_citacion = id_citacion
        self.fecha_programada = fecha_programada
        self.correo_destinatarios: List[str] = []
        self.motivo = motivo
        self.descripcion = descripcion
        self.lugar = lugar
        self.id_remitente = id_remitente
        self.id_entrevista = id_entrevista
        self.notificaciones: List['Notificacion'] = []
    @property
    def correo_destinatarios(self) -> List[str]:
        return self.correo_destinatarios.copy()
    @property
    def notificaciones(self) -> List['Notificacion']:
        return self.notificaciones.copy()

    def agregar_destinatario(self, correo: str) -> None:
        if correo not in self.correo_destinatarios:
            self.correo_destinatarios.append(correo)

    def eliminar_destinatario(self, correo: str) -> None:
        if correo in self.correo_destinatarios:
            self.correo_destinatarios.remove(correo)

    def agregar_notificacion(self, notificacion: 'Notificacion') -> None:
        if notificacion not in self.notificaciones:
            self.notificaciones.append(notificacion)
