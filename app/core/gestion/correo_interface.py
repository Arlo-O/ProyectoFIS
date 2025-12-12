from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class IEnvioCorreo(ABC):
    @abstractmethod
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        pass

    @abstractmethod
    def enviar_masivo(self, destinatarios: List[str], asunto: str, contenido: str) -> Dict[str, bool]:
        pass
