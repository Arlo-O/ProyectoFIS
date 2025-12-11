from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..usuarios.directivo import Directivo
    from .logro import Logro


class CategoriaLogro:
    def __init__(self, id_categoria: int, nombre: str, descripcion: str, 
                 id_creador: Optional[int] = None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_creador = id_creador
        self.logros: List['Logro'] = []
    @property
    def logros(self) -> List['Logro']:
        return self.logros.copy()
