# 🔐 Servicio RBAC - Control de Acceso Basado en Roles

from typing import Optional, List
from functools import wraps
import tkinter.messagebox as messagebox

class RBACService:
    """
    Servicio de Control de Acceso Basado en Roles (RBAC)
    Valida permisos y controla acceso a funcionalidades
    """
    
    def __init__(self):
        self.current_user = None
        self.current_role = None
        self.current_permissions = []
    
    def set_user_context(self, usuario, role_name: str, permissions: List[str]):
        """
        Establece el contexto del usuario actual con sus permisos
        
        Args:
            usuario: Instancia de Usuario desde la autenticación
            role_name: Nombre del rol (ej: "Profesor")
            permissions: Lista de nombres de permisos (ej: ["ver_calificaciones", "crear_grupos"])
        """
        self.current_user = usuario
        self.current_role = role_name
        self.current_permissions = permissions
        
        print(f"[RBAC] Usuario {usuario.correo_electronico} con rol {role_name}")
        print(f"[RBAC] Permisos asignados: {permissions}")
    
    def tiene_permiso(self, nombre_permiso: str) -> bool:
        """
        Verifica si el usuario actual tiene un permiso específico
        
        Args:
            nombre_permiso: Nombre del permiso (ej: "acceder_admin")
        
        Returns:
            True si tiene el permiso, False en caso contrario
        """
        if not self.current_user:
            print("[RBAC] No hay usuario autenticado")
            return False
        
        tiene = nombre_permiso in self.current_permissions
        print(f"[RBAC] Verificando permiso '{nombre_permiso}': {tiene}")
        return tiene
    
    def tiene_alguno_de(self, permisos: List[str]) -> bool:
        """
        Verifica si el usuario tiene al menos uno de los permisos especificados
        
        Args:
            permisos: Lista de nombres de permisos
        
        Returns:
            True si tiene al menos uno, False en caso contrario
        """
        for permiso in permisos:
            if self.tiene_permiso(permiso):
                return True
        return False
    
    def tiene_todos(self, permisos: List[str]) -> bool:
        """
        Verifica si el usuario tiene todos los permisos especificados
        
        Args:
            permisos: Lista de nombres de permisos
        
        Returns:
            True si tiene todos, False en caso contrario
        """
        for permiso in permisos:
            if not self.tiene_permiso(permiso):
                return False
        return True
    
    def validar_acceso(self, nombre_permiso: str, mensaje_error: str = None) -> bool:
        """
        Valida acceso y muestra mensaje de error si no tiene permiso
        
        Args:
            nombre_permiso: Nombre del permiso a validar
            mensaje_error: Mensaje personalizado de error (opcional)
        
        Returns:
            True si tiene permiso, False en caso contrario
        """
        if self.tiene_permiso(nombre_permiso):
            return True
        
        # Mostrar error
        error_msg = mensaje_error or f"No tienes permiso para acceder a esta funcionalidad"
        messagebox.showerror(
            "Acceso Denegado",
            f"❌ Acceso Denegado\n\n{error_msg}"
        )
        return False
    
    def obtener_permisos(self) -> List[str]:
        """Retorna la lista de permisos del usuario actual"""
        return self.current_permissions.copy()
    
    def obtener_rol(self) -> Optional[str]:
        """Retorna el rol actual del usuario"""
        return self.current_role
    
    def obtener_usuario(self):
        """Retorna el usuario actual"""
        return self.current_user
    
    def limpiar_contexto(self):
        """Limpia el contexto del usuario (para logout)"""
        self.current_user = None
        self.current_role = None
        self.current_permissions = []
        print("[RBAC] Contexto limpiado")


# Instancia global del servicio RBAC
rbac_service = RBACService()


def require_permission(nombre_permiso: str):
    """
    Decorador para proteger funciones que requieren un permiso específico
    
    Uso:
        @require_permission("acceder_admin")
        def create_admin_dashboard(parent):
            ...
    
    Si el usuario no tiene el permiso:
    - Se muestra un mensaje de error
    - La función NO se ejecuta
    - Se retorna None
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not rbac_service.tiene_permiso(nombre_permiso):
                messagebox.showerror(
                    "Acceso Denegado",
                    f"❌ No tienes permiso para acceder a esta sección.\n\n"
                    f"Permiso requerido: {nombre_permiso}\n"
                    f"Rol actual: {rbac_service.obtener_rol()}"
                )
                return None
            
            print(f"[RBAC] Acceso permitido a {func.__name__} para {nombre_permiso}")
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_any_permission(*permisos):
    """
    Decorador para proteger funciones que requieren CUALQUIERA de varios permisos
    
    Uso:
        @require_any_permission("acceder_admin", "acceder_director")
        def create_dashboard(parent):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not rbac_service.tiene_alguno_de(list(permisos)):
                messagebox.showerror(
                    "Acceso Denegado",
                    f"❌ No tienes permiso para acceder a esta sección.\n\n"
                    f"Permisos requeridos: {', '.join(permisos)}\n"
                    f"Tus permisos: {', '.join(rbac_service.obtener_permisos()) or 'ninguno'}"
                )
                return None
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_all_permissions(*permisos):
    """
    Decorador para proteger funciones que requieren TODOS los permisos especificados
    
    Uso:
        @require_all_permissions("ver_estudiantes", "ver_calificaciones")
        def create_student_dashboard(parent):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not rbac_service.tiene_todos(list(permisos)):
                messagebox.showerror(
                    "Acceso Denegado",
                    f"❌ No tienes los permisos requeridos.\n\n"
                    f"Permisos requeridos: {', '.join(permisos)}\n"
                    f"Tus permisos: {', '.join(rbac_service.obtener_permisos()) or 'ninguno'}"
                )
                return None
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
