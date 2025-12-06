"""
Archivo: session_manager.py
Gestión del estado de la sesión de usuario activa.

Este módulo mantiene el estado global de la sesión del usuario, específicamente
su rol (admin, director, teacher, parent). Se utiliza para:
- Determinar qué dashboard mostrar después del login
- Controlar permisos y acceso a diferentes módulos
- Gestionar la navegación contextual según el rol

Nota: En una aplicación real, esto debería expandirse para incluir
más información del usuario (ID, nombre, permisos específicos, etc.)
"""

# ======================================================================
# ESTADO GLOBAL DE SESIÓN
# ======================================================================

# Variable privada que almacena el rol del usuario actual
# Valores posibles: "admin", "director", "teacher", "parent", None
_current_role = None

# ======================================================================
# FUNCIONES DE GESTIÓN DE SESIÓN
# ======================================================================

def set_current_role(role):
    """
    Establece el rol del usuario que ha iniciado sesión.
    
    Esta función se llama inmediatamente después de una autenticación exitosa
    para registrar el tipo de usuario que está usando la aplicación.
    
    Parámetros:
        role (str): Rol del usuario ('admin', 'director', 'teacher', 'parent')
    """
    global _current_role
    _current_role = role

def get_current_role():
    """
    Obtiene el rol del usuario actualmente autenticado.
    
    Retorna:
        str|None: El rol del usuario actual, o None si no hay sesión activa
    """
    return _current_role

def get_dashboard_command(nav_commands):
    """
    Determina el comando de navegación apropiado para volver al dashboard
    del usuario actual.
    
    Esta función es útil para botones de "Volver al inicio" que deben llevar
    al usuario a SU dashboard específico según su rol.
    
    Parámetros:
        nav_commands (dict): Diccionario con todas las funciones de navegación
                            disponibles (ej: {'dashboard_home': lambda: ..., })
    
    Retorna:
        function: Función lambda para navegar al dashboard correspondiente
    
    Ejemplo de uso:
        home_btn = ttk.Button(frame, text="Inicio",
                             command=get_dashboard_command(nav_commands))
    """
    role = get_current_role()
    
    # Mapeo de roles a comandos de navegación
    if role == "admin":
        return nav_commands['dashboard_home']
    elif role == "director":
        return nav_commands['director_home']
    elif role == "teacher":
        return nav_commands['teacher_home']
    elif role == "parent":
        return nav_commands['parent_home']
    else:
        # Si no hay sesión activa o rol desconocido, volver al login
        return nav_commands['home']