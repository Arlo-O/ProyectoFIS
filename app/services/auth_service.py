from typing import Optional, Tuple, List
from app.data.uow import uow
from app.core.usuarios.usuario import Usuario
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.acudiente import Acudiente
from app.core.usuarios.administrador import Administrador
import sqlalchemy as sa
import bcrypt


def cargar_persona_usuario(unit_of_work, usuario: Usuario):
    """
    Carga los datos de Persona asociados al Usuario.
    
    - Si usuario es Administrador (hereda de Usuario), ya tiene sus propios datos
    - Si no, busca en Profesor/Directivo/Acudiente (heredan de Persona, tienen FK a Usuario)
    """
    try:
        # Si usuario ya es Administrador (herencia), usar sus propios datos
        if isinstance(usuario, Administrador):
            usuario.persona = usuario  # El administrador ES el usuario con datos propios
            print(f"DEBUG: Usuario es Administrador: {usuario.primer_nombre} {usuario.primer_apellido}")
            return
        
        # Buscar en Profesor
        try:
            profesor = unit_of_work.session.query(Profesor).filter(
                Profesor.id_usuario == usuario.id_usuario
            ).first()
            if profesor:
                usuario.persona = profesor
                print(f"DEBUG: Persona cargada (Profesor): {profesor.primer_nombre}")
                return
        except Exception as e:
            print(f"DEBUG: Error buscando en Profesor: {str(e)}")
        
        # Buscar en Directivo
        try:
            directivo = unit_of_work.session.query(Directivo).filter(
                Directivo.id_usuario == usuario.id_usuario
            ).first()
            if directivo:
                usuario.persona = directivo
                print(f"DEBUG: Persona cargada (Directivo): {directivo.primer_nombre}")
                return
        except Exception as e:
            print(f"DEBUG: Error buscando en Directivo: {str(e)}")
        
        # Buscar en Acudiente
        try:
            acudiente = unit_of_work.session.query(Acudiente).filter(
                Acudiente.id_usuario == usuario.id_usuario
            ).first()
            if acudiente:
                usuario.persona = acudiente
                print(f"DEBUG: Persona cargada (Acudiente): {acudiente.primer_nombre}")
                return
        except Exception as e:
            print(f"DEBUG: Error buscando en Acudiente: {str(e)}")
        
        print(f"DEBUG: No se encontró Persona asociada, usando email como identificador")
        
    except Exception as e:
        print(f"DEBUG: Error cargando Persona: {str(e)}")


def obtener_permisos_usuario(usuario, session) -> List[str]:
    """
    Obtiene la lista de nombres de permisos de un usuario basado en su rol
    MEDIANTE QUERY DIRECTO A LA BASE DE DATOS
    
    Args:
        usuario: Instancia de Usuario
        session: Sesión de SQLAlchemy activa
    
    Returns:
        Lista de nombres de permisos
    """
    permisos = []
    
    try:
        if not usuario.id_rol:
            print(f"[AUTH] Usuario {usuario.correo_electronico} no tiene rol asignado")
            return permisos
        
        # Query DIRECTO para obtener permisos del rol
        from sqlalchemy import text
        query = text("""
            SELECT p.nombre 
            FROM permiso p
            JOIN rol_permiso rp ON p.id_permiso = rp.id_permiso
            WHERE rp.id_rol = :rol_id
        """)
        
        result = session.execute(query, {"rol_id": usuario.id_rol})
        permisos = [row[0] for row in result.fetchall()]
        
        print(f"[AUTH] Permisos cargados para rol {usuario.id_rol}: {permisos}")
        
    except Exception as e:
        print(f"[AUTH] Error obteniendo permisos: {e}")
        import traceback
        traceback.print_exc()
    
    return permisos


class AuthenticationService:
    @staticmethod
    def verify_password(password_ingresada: str, password_hash: str) -> bool:
        """
        Verifica que la contraseña ingresada coincida con el hash almacenado.
        Usa bcrypt para la verificación segura.
        """
        try:
            return bcrypt.checkpw(
                password_ingresada.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception as e:
            print(f"ERROR verificando contraseña: {e}")
            return False

    @staticmethod
    def authenticate(email: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario contra la base de datos.
        Carga TODAS las relaciones DENTRO del context manager para evitar DetachedInstanceError.
        """
        try:
            with uow() as unit_of_work:
                # ✅ Obtener el usuario
                usuario = unit_of_work.usuarios.get_by_email(email)
                
                if usuario is None:
                    print(f"DEBUG: Usuario con email '{email}' no encontrado")
                    return None
                
                print(f"DEBUG: Usuario encontrado: {usuario}")
                print(f"DEBUG: Tipo de usuario: {type(usuario)}")
                
                # Verificar contraseña usando bcrypt
                if not AuthenticationService.verify_password(password, usuario.contrasena):
                    print(f"DEBUG: Contraseña incorrecta para {email}")
                    return None
                
                print(f"DEBUG: Contraseña correcta para {email}")
                
                # ✅ Cargar la Persona asociada al Usuario DENTRO de la sesión
                cargar_persona_usuario(unit_of_work, usuario)
                
                # ✅ CARGAR ROL Y PERMISOS ANTES DE SALIR DE LA SESIÓN
                try:
                    # Forzar la carga del rol dentro de la sesión
                    rol = usuario.rol
                    if rol:
                        print(f"DEBUG: Rol cargado: {rol}")
                        nombre_rol = rol.nombre_rol
                        print(f"DEBUG: Nombre del rol: {nombre_rol}")
                        
                        # ✅ Cargar permisos mediante query directo
                        permisos = obtener_permisos_usuario(usuario, unit_of_work.session)
                        print(f"DEBUG: Permisos cargados: {permisos}")
                        usuario._permisos = permisos
                    else:
                        print(f"DEBUG: Usuario {email} no tiene rol asignado")
                        usuario._permisos = []
                        
                except Exception as e:
                    print(f"DEBUG: Error cargando rol/permisos: {str(e)}")
                    usuario._permisos = []
                
                # ✅ CRUCIAL: Desacoplar el usuario de la sesión pero mantener sus atributos cargados
                # Hacer que SQLAlchemy expanda/serialice todos los atributos antes de salir
                unit_of_work.session.expunge(usuario)
                
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