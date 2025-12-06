# Subpaquete de modelos de logros
# Exporta todas las clases de logros académicos

from .logro import Logro
from .categoriaLogro import CategoriaLogro
from .evaluacionLogro import EvaluacionLogro
from .boletin import Boletin

__all__ = [
    'Logro',
    'CategoriaLogro',
    'EvaluacionLogro',
    'Boletin'
]
