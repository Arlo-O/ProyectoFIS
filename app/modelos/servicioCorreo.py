from .iEnvioCorreo import IEnvioCorreo

class ServicioCorreo(IEnvioCorreo):
    def __init__(self, servidor: str = None, puerto: int = None, usuario: str = None):
        self.__servidor = servidor
        self.__puerto = puerto
        self.__usuario = usuario

    def enviar(self, destinatario: str, asunto: str, cuerpo: str, adjuntos: list = None) -> bool:
        # implementación de prueba (no envía correos realmente)
        try:
            # se podría integrar con smtplib u otra librería
            print(f"Enviar correo a {destinatario}: {asunto}")
            return True
        except Exception:
            return False

    def enviarMasivo(self, destinatarios: list, asunto: str, cuerpo: str) -> dict:
        resultados = {}
        for d in destinatarios:
            resultados[d] = self.enviar(d, asunto, cuerpo)
        return resultados