from typing import List, Protocol

class IEnvioCorreo(Protocol):
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        ...

class ServicioNotificaciones:
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        """
        Simulates sending an email.
        In a real implementation, this would use SMTP.
        """
        print(f"--- SIMULACIÓN DE ENVÍO DE CORREO ---")
        print(f"Para: {', '.join(destinatarios)}")
        print(f"Asunto: {asunto}")
        print(f"Contenido: {contenido}")
        print(f"-------------------------------------")
        return True
