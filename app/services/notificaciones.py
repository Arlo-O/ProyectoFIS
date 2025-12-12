from typing import List, Protocol
from abc import ABC, abstractmethod


class IEnvioCorreo(Protocol):
    @abstractmethod
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        ...


class ServicioNotificaciones(IEnvioCorreo):
    
    def enviar_correo(self, destinatarios: List[str], asunto: str, contenido: str) -> bool:
        print("--- SIMULACIÓN DE ENVÍO DE CORREO ---")
        print(f"Para: {', '.join(destinatarios)}")
        print(f"Asunto: {asunto}")
        print(f"Contenido: {contenido[:100]}{'...' if len(contenido) > 100 else ''}")
        print("-" * 37)
        return True


def procesar_notificacion(servicio_envio: IEnvioCorreo, destinatarios: List[str], 
                         asunto: str, contenido: str) -> bool:
    return servicio_envio.enviar_correo(destinatarios, asunto, contenido)
