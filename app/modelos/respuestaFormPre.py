class RespuestaFormPre:
    def __init__(self, idRespuesta: int = None, formato: str = None, contenido: str = None, remitente: str = None):
        self.__idRespuesta: int = idRespuesta
        self.__formato: str = formato
        self.__contenido: str = contenido
        self.__remitente: str = remitente

    @property
    def idRespuesta(self) -> int:
        return self.__idRespuesta

    @property
    def formato(self) -> str:
        return self.__formato

    @property
    def contenido(self) -> str:
        return self.__contenido

    def resumen(self) -> str:
        return f"Respuesta {self.__idRespuesta} - Formato: {self.__formato}"