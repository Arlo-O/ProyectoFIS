from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from ..logros.categoriaLogro import CategoriaLogro


class Logro:
    def __init__(self, id_logro: int, titulo: str, descripcion: str, 
                 fecha_creacion: datetime, estado: str, id_creador: Optional[int] = None,
                 id_categoria: Optional[int] = None):
        self.id_logro = id_logro
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.estado = estado
        self.id_creador = id_creador
        self.id_categoria = id_categoria



