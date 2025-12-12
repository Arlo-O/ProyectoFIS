from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional


if TYPE_CHECKING:
    from ..usuarios.profesor import Profesor


class Anotacion:
    def __init__(self, id_anotacion: int, fecha: datetime, descripcion: str, 
                 autor: Optional['Profesor'], tipo: str, id_observador: Optional[int] = None):
        self.id_anotacion = id_anotacion
        self.fecha = fecha
        self.descripcion = descripcion
        self.autor = autor
        self.tipo = tipo
        self.id_observador = id_observador
