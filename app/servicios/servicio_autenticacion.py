import bcrypt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


class ServicioAutenticacion:
    """Servicio de autenticación y validación de credenciales"""
    
    MAX_INTENTOS_FALLIDOS = 3
    DURACION_BLOQUEO_MINUTOS = 15
    
    def __init__(self):
        self.intentos_fallidos = {}  # {username: {contador: int, bloqueado_hasta: datetime}}
    
    def cifrar_contrasena(self, contrasena: str) -> str:
        """Cifra una contraseña usando bcrypt"""
        return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verificar_contrasena(self, contrasena_ingresada: str, contrasena_cifrada: str) -> bool:
        """Verifica que la contraseña ingresada coincida con la cifrada"""
        try:
            return bcrypt.checkpw(contrasena_ingresada.encode('utf-8'), contrasena_cifrada.encode('utf-8'))
        except Exception:
            return False
    
    def verificar_bloqueado(self, username: str) -> bool:
        """Verifica si la cuenta está bloqueada por intentos fallidos"""
        if username not in self.intentos_fallidos:
            return False
        
        info = self.intentos_fallidos[username]
        if info['bloqueado_hasta'] and datetime.now() < info['bloqueado_hasta']:
            return True
        
        # Desbloquear si pasó el tiempo
        if info['bloqueado_hasta'] and datetime.now() >= info['bloqueado_hasta']:
            self.intentos_fallidos[username] = {'contador': 0, 'bloqueado_hasta': None}
        
        return False
    
    def registrar_intento_fallido(self, username: str):
        """Registra un intento fallido de login"""
        if username not in self.intentos_fallidos:
            self.intentos_fallidos[username] = {'contador': 0, 'bloqueado_hasta': None}
        
        self.intentos_fallidos[username]['contador'] += 1
        
        if self.intentos_fallidos[username]['contador'] >= self.MAX_INTENTOS_FALLIDOS:
            self.intentos_fallidos[username]['bloqueado_hasta'] = datetime.now() + timedelta(minutes=self.DURACION_BLOQUEO_MINUTOS)
    
    def registrar_intento_exitoso(self, username: str):
        """Limpia los intentos fallidos después de login exitoso"""
        if username in self.intentos_fallidos:
            self.intentos_fallidos[username] = {'contador': 0, 'bloqueado_hasta': None}
    
    def obtener_mensajes_bloqueo(self, username: str) -> str:
        """Obtiene el mensaje de bloqueo con tiempo restante"""
        if username not in self.intentos_fallidos:
            return ""
        
        info = self.intentos_fallidos[username]
        if info['bloqueado_hasta']:
            tiempo_restante = info['bloqueado_hasta'] - datetime.now()
            minutos = tiempo_restante.seconds // 60
            segundos = tiempo_restante.seconds % 60
            return f"Cuenta bloqueada. Reintentar en {minutos}m {segundos}s"
        
        return ""
