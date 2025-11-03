from .igeneradorPDF import IGeneradorPDF

class GeneradorPDF(IGeneradorPDF):
    def __init__(self):
        pass

    def generarPDF(self, fuente: str, destino: str, opciones: dict = None) -> bytes:
        # implementación mínima que simula la generación de un PDF
        contenido = f"PDF generado desde {fuente} con opciones {opciones}".encode("utf-8")
        return contenido

    def exportar(self, contenido: bytes, ruta: str) -> None:
        with open(ruta, "wb") as f:
            f.write(contenido)