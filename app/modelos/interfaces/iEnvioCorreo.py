from abc import ABC, abstractmethod

class IEnvioCorreo(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, asunto: str, cuerpo: str, adjuntos: list = None) -> bool:
        pass

    @abstractmethod
    def enviarMasivo(self, destinatarios: list, asunto: str, cuerpo: str) -> dict:
        pass