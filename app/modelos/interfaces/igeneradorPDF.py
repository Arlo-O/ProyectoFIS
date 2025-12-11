from abc import ABC, abstractmethod
from typing import Dict, Optional


class IGeneradorPDF(ABC):
    @abstractmethod
    def generar_pdf(self, fuente: str, opciones: Optional[Dict] = None) -> bytes:
        pass

    @abstractmethod
    def guardar_pdf(self, contenido: bytes, ruta: str) -> None:
        pass
