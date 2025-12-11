from typing import Dict, Optional


class PlantillaNotificacion:
    def __init__(self, id_plantilla: Optional[int] = None, nombre: str = "", 
                 asunto: str = "", cuerpo: str = ""):
        self.__id_plantilla = id_plantilla
        self.__nombre = nombre
        self.__asunto = asunto
        self.__cuerpo = cuerpo

    @property
    def id_plantilla(self) -> Optional[int]:
        return self.__id_plantilla

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def cuerpo(self) -> str:
        return self.__cuerpo

    def render(self, context: Optional[Dict[str, any]] = None) -> str:
        body = self.__cuerpo or ""
        context = context or {}
        for key, value in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return body
