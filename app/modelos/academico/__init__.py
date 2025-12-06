# Subpaquete de modelos académicos
# Exporta todas las clases académicas

from .grupo import Grupo
from .grado import Grado
from .periodoAcademico import PeriodoAcademico
from .hojaVidaAcademica import HojaVidaAcademica
from .observador import Observador
from .anotacion import Anotacion

__all__ = [
    'Grupo',
    'Grado',
    'PeriodoAcademico',
    'HojaVidaAcademica',
    'Observador',
    'Anotacion'
]
