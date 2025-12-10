from typing import List, Protocol

class IEnvioCorreo(Protocol):
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        """Envía un correo electrónico a los destinatarios especificados.
        
        Returns:
            bool: True si el envío fue exitoso, False en caso contrario
        """
        ...

class ServicioNotificaciones:
    """Servicio para el envío de notificaciones por correo electrónico."""
    
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        """Simula el envío de un correo electrónico.
        
        Returns:
            bool: Siempre retorna True en modo simulación
        """
        print(f"--- SIMULACIÓN DE ENVÍO DE CORREO ---")
        print(f"Para: {', '.join(destinatarios)}")
        print(f"Asunto: {asunto}")
        print(f"Contenido: {contenido}")
        print(f"{'-'*37}")
        return True
