from typing import Dict, Optional


class PlantillaNotificacion:
    def __init__(self, id_plantilla: Optional[int] = None, nombre: str = "", 
                 asunto: str = "", cuerpo: str = ""):
        self.id_plantilla = id_plantilla
        self.nombre = nombre
        self.asunto = asunto
        self.cuerpo = cuerpo
    def render(self, context: Optional[Dict[str, any]] = None) -> str:
        body = self.cuerpo or ""
        context = context or {}
        for key, value in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return body
