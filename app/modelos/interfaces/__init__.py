# Subpaquete de interfaces
# Exporta todas las interfaces del sistema

from .iEnvioCorreo import IEnvioCorreo
from .igeneradorPDF import IGeneradorPDF

__all__ = [
    'IEnvioCorreo',
    'IGeneradorPDF'
]
