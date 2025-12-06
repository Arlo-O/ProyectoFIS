class PlantillaNotificacion:
    def __init__(self, idPlantilla: int = None, nombre: str = None, asunto: str = None, cuerpo: str = None):
        self.__idPlantilla: int = idPlantilla
        self.__nombre: str = nombre
        self.__asunto: str = asunto
        self.__cuerpo: str = cuerpo

    @property
    def idPlantilla(self) -> int:
        return self.__idPlantilla

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def cuerpo(self) -> str:
        return self.__cuerpo

    def render(self, context: dict) -> str:
        body = self.__cuerpo or ""
        for k, v in (context or {}).items():
            body = body.replace("{{%s}}" % k, str(v))
        return body
