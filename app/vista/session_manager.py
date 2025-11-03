# Archivo: session_manager.py

"""
Módulo para gestionar el estado de la sesión activa (rol del usuario).
"""

_current_role = None

def set_current_role(role):
    """Establece el rol del usuario actualmente autenticado."""
    global _current_role
    _current_role = role

def get_current_role():
    """Obtiene el rol del usuario actualmente autenticado."""
    return _current_role

def get_dashboard_command(nav_commands):
    """
    Retorna el comando de navegación correcto (lambda function) basado
    en el rol actual de la sesión.
    """
    role = get_current_role()
    
    if role == "admin":
        return nav_commands['dashboard_home']
    elif role == "director":
        return nav_commands['director_home']
    elif role == "teacher":
        return nav_commands['teacher_home']
    elif role == "parent":
        return nav_commands['parent_home']
    else:
        # Por defecto, si no hay rol, vuelve al login.
        return nav_commands['home']