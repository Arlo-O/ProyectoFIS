"""
session_manager.py
Gestión del estado de la sesión de usuario activa.
"""

_current_role = None

_user_info = {
    "id": None,
    "name": None,
    "email": None,
    "role": None,
    "department": None,
    "permissions": []
}


def set_current_role(role):
    global _current_role
    _current_role = role


def get_current_role():
    return _current_role


def set_user_info(user_id, name, email, role, department=None, permissions=None):
    global _user_info, _current_role
    
    _user_info = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "department": department,
        "permissions": permissions if permissions else []
    }
    _current_role = role


def get_user_info():
    return _user_info.copy()


def get_user_name():
    return _user_info["name"]


def get_user_id():
    return _user_info["id"]


def get_user_department():
    return _user_info["department"]


def has_permission(permission):
    return permission in _user_info["permissions"]


def clear_session():
    global _current_role, _user_info
    
    # ✅ NUEVO: Limpiar contexto RBAC también
    try:
        from app.services.rbac_service import rbac_service
        rbac_service.limpiar_contexto()
    except Exception as e:
        print(f"[⚠️ ] Error limpiando RBAC: {e}")
    
    _current_role = None
    _user_info = {
        "id": None,
        "name": None,
        "email": None,
        "role": None,
        "department": None,
        "permissions": []
    }


def is_authenticated():
    return _current_role is not None and _user_info["id"] is not None


def is_admin():
    return _current_role == "admin"


def is_director():
    return _current_role == "director"


def is_teacher():
    return _current_role == "teacher"


def is_parent():
    return _current_role == "parent"


def get_dashboard_command(nav_commands):
    role = get_current_role()
    
    if role == "admin":
        return nav_commands.get('dashboard_home', nav_commands['home'])
    elif role == "director":
        return nav_commands.get('director_home', nav_commands['home'])
    elif role == "teacher":
        return nav_commands.get('teacher_home', nav_commands['home'])
    elif role == "parent":
        return nav_commands.get('parent_home', nav_commands['home'])
    else:
        return nav_commands.get('home', lambda: None)


def log_session_info():
    print("="*50)
    print("INFORMACIÓN DE SESIÓN ACTUAL")
    print("="*50)
    print(f"Rol: {_current_role}")
    print(f"Usuario ID: {_user_info['id']}")
    print(f"Nombre: {_user_info['name']}")
    print(f"Email: {_user_info['email']}")
    print(f"Departamento: {_user_info['department']}")
    print(f"Permisos: {_user_info['permissions']}")
    print(f"Autenticado: {is_authenticated()}")
    print("="*50)


ROLE_ADMIN = "admin"
ROLE_DIRECTOR = "director"
ROLE_TEACHER = "teacher"
ROLE_PARENT = "parent"

ROLE_PERMISSIONS = {
    ROLE_ADMIN: [
        'manage_users',
        'manage_roles',
        'manage_courses',
        'gle',
        'observer',
        'attendance',
        'reports',
        'settings',
        'audit_logs'
    ],
    ROLE_DIRECTOR: [
        'manage_teachers',
        'manage_courses',
        'view_reports',
        'attendance_reports',
        'gle_reports',
        'view_students'
    ],
    ROLE_TEACHER: [
        'gle',
        'observer',
        'attendance',
        'create_reports',
        'view_students',
        'manage_group'
    ],
    ROLE_PARENT: [
        'view_grades',
        'view_attendance',
        'view_reports',
        'view_observations',
        'message_teacher'
    ]
}


def get_role_permissions(role):
    return ROLE_PERMISSIONS.get(role, [])


def validate_role(role):
    return role in ROLE_PERMISSIONS.keys()
