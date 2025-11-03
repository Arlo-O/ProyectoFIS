from abc import ABC, abstractmethod

class IGeneradorPDF(ABC):
    @abstractmethod
    def generarPDF(self, fuente: str, destino: str, opciones: dict = None) -> bytes:
        """Genera un PDF a partir de una fuente (plantilla, datos) y devuelve el contenido binario."""
        pass

    @abstractmethod
    def exportar(self, contenido: bytes, ruta: str) -> None:
        pass