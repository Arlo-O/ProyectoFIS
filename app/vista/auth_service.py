from typing import Optional, Tuple
from app.infraestructura.uow import uow
from app.modelos.usuarios.usuario import Usuario


class AuthenticationService:
    @staticmethod
    def authenticate(email: str, password: str) -> Optional[Usuario]:
        try:
            with uow() as unit_of_work:
                usuario = unit_of_work.usuarios.get_by_email(email)
                if usuario is None:
                    return None
                if usuario.contrasena == password:
                    return usuario
                return None
                    
        except Exception as e:
            print(f"Error durante autenticación: {str(e)}")
            raise

    @staticmethod
    def validate_credentials(email: str, password: str) -> Tuple[bool, Optional[str]]:
        if not email or not email.strip():
            return False, "Usuario no puede estar vacío."
        
        if not password or not password.strip():
            return False, "Contraseña no puede estar vacía."
        
        return True, None
