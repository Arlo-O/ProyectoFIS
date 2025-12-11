from typing import Optional, Tuple
from app.infraestructura.uow import uow
from app.modelos.usuarios.usuario import Usuario
import sqlalchemy as sa



class AuthenticationService:
    @staticmethod
    def authenticate(email: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario contra la base de datos.
        Maneja herencia polimórfica de SQLAlchemy correctamente.
        """
        try:
            with uow() as unit_of_work:
                # ✅ Usar filter_by() en lugar de filter() para evitar problemas de mapeo
                usuario = unit_of_work.usuarios.get_by_email(email)
                
                if usuario is None:
                    print(f"DEBUG: Usuario con email '{email}' no encontrado")
                    return None
                
                print(f"DEBUG: Usuario encontrado: {usuario}")
                print(f"DEBUG: Tipo de usuario: {type(usuario)}")
                
                # Verificar contraseña
                if usuario.contrasena != password:
                    print(f"DEBUG: Contraseña incorrecta para {email}")
                    return None
                
                print(f"DEBUG: Contraseña correcta para {email}")
                
                # ✅ IMPORTANTE: Cargar la relación rol ANTES de salir del context manager
                # Esto evita problemas de lazy loading después de cerrar la sesión
                try:
                    rol = usuario.rol
                    if rol:
                        print(f"DEBUG: Rol cargado: {rol}")
                        # Acceder a atributos del rol para forzar la carga
                        _ = rol.nombre_rol
                    else:
                        print(f"DEBUG: Usuario {email} no tiene rol asignado")
                except Exception as e:
                    print(f"DEBUG: Error cargando rol: {str(e)}")
                
                return usuario
                    
        except Exception as e:
            print(f"ERROR durante autenticación: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


    @staticmethod
    def validate_credentials(email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que las credenciales tengan un formato correcto.
        No valida contra la BD, solo verifica que no estén vacías.
        """
        if not email or not email.strip():
            return False, "Usuario no puede estar vacío."
        
        if not password or not password.strip():
            return False, "Contraseña no puede estar vacía."
        
        # Validar formato de email básico
        if "@" not in email or "." not in email:
            return False, "El email no tiene un formato válido."
        
        return True, None
