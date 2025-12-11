from sqlalchemy.orm import Session
from ..repositorios import RepositorioUsuario
from .servicio_autenticacion import ServicioAutenticacion


class ControladorLogin:
    """Controlador que maneja el proceso de autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repositorio_usuario = RepositorioUsuario(db)
        self.servicio_autenticacion = ServicioAutenticacion()
    
    def autenticar_usuario(self, username: str, contrasena: str) -> dict:
        """
        Autentica un usuario y retorna su información si es válido
        
        Retorna:
            {
                'exitoso': bool,
                'usuario': Usuario|None,
                'rol': Rol|None,
                'mensaje': str
            }
        """
        
        # 1. Verificar si cuenta está bloqueada
        if self.servicio_autenticacion.verificar_bloqueado(username):
            mensaje_bloqueo = self.servicio_autenticacion.obtener_mensajes_bloqueo(username)
            return {
                'exitoso': False,
                'usuario': None,
                'rol': None,
                'mensaje': mensaje_bloqueo
            }
        
        # 2. Consultar usuario por username (email)
        usuario = self.repositorio_usuario.obtener_por_email(username)
        
        if not usuario:
            self.servicio_autenticacion.registrar_intento_fallido(username)
            return {
                'exitoso': False,
                'usuario': None,
                'rol': None,
                'mensaje': 'Usuario o contraseña incorrectos'
            }
        
        # 3. Verificar que usuario esté activo
        if not usuario.activo:
            self.servicio_autenticacion.registrar_intento_fallido(username)
            return {
                'exitoso': False,
                'usuario': None,
                'rol': None,
                'mensaje': 'Usuario desactivado'
            }
        
        # 4. Validar contraseña cifrada
        if not self.servicio_autenticacion.verificar_contrasena(contrasena, usuario.contrasenaEncriptada):
            self.servicio_autenticacion.registrar_intento_fallido(username)
            intentos_restantes = self.servicio_autenticacion.MAX_INTENTOS_FALLIDOS - self.servicio_autenticacion.intentos_fallidos[username]['contador']
            
            return {
                'exitoso': False,
                'usuario': None,
                'rol': None,
                'mensaje': f'Usuario o contraseña incorrectos ({intentos_restantes} intentos restantes)'
            }
        
        # 5. Credenciales válidas - obtener rol
        self.servicio_autenticacion.registrar_intento_exitoso(username)
        
        rol = usuario.rol if usuario.rol else None
        
        return {
            'exitoso': True,
            'usuario': usuario,
            'rol': rol,
            'mensaje': f'Bienvenido {username}'
        }
    
    def obtener_modulo_por_rol(self, rol_nombre: str) -> str:
        """Retorna el nombre del módulo según el rol del usuario"""
        rol_modulo_map = {
            'admin': 'admin',
            'administrator': 'admin',
            'directivo': 'director',
            'director': 'director',
            'profesor': 'teacher',
            'teacher': 'teacher',
            'acudiente': 'parent',
            'parent': 'parent',
            'observador': 'observer',
            'observer': 'observer',
        }
        
        return rol_modulo_map.get(rol_nombre.lower(), 'teacher')
