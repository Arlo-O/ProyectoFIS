#!/usr/bin/env python
"""
scripts/insert_test_users.py

Script para insertar usuarios de prueba en la BD.
Ejecutar UNA SOLA VEZ al inicializar el ambiente de desarrollo.

Uso:
    python scripts/insert_test_users.py
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Agregar la ruta del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.infraestructura.uow import uow
from app.modelos.usuarios.persona import Persona
from app.modelos.usuarios.usuario import Usuario
from app.modelos.usuarios.rol import Rol


def get_or_create_role(unit_of_work, role_name: str, description: str) -> Rol:
    """
    Obtiene un rol existente o lo crea si no existe.
    
    Args:
        unit_of_work: UnitOfWork instance
        role_name: nombre del rol
        description: descripción del rol
    
    Returns:
        Instancia de Rol
    """
    role = unit_of_work.session.query(Rol).filter_by(nombre_rol=role_name).first()
    if not role:
        role = Rol(nombre_rol=role_name, descripcion_rol=description)
        unit_of_work.session.add(role)
    return role


def insert_test_users():
    """Inserta usuarios de prueba en la BD desde .env"""
    
    print("=" * 70)
    print("Insertando usuarios de prueba en la BD...")
    print("=" * 70)
    
    # Usuarios a insertar desde .env
    test_users = [
        {
            "email": os.getenv("TEST_ADMIN_EMAIL", "admin@colegio.edu"),
            "password": os.getenv("TEST_ADMIN_PASSWORD", "admin123"),
            "nombre": "Admin",
            "apellido": "Usuario",
            "rol_name": "administrador",
            "rol_desc": "Administrador del sistema",
        },
        {
            "email": os.getenv("TEST_DIRECTOR_EMAIL", "director@colegio.edu"),
            "password": os.getenv("TEST_DIRECTOR_PASSWORD", "dir123"),
            "nombre": "Director",
            "apellido": "Usuario",
            "rol_name": "director",
            "rol_desc": "Director de la institución",
        },
        {
            "email": os.getenv("TEST_TEACHER_EMAIL", "profesor@colegio.edu"),
            "password": os.getenv("TEST_TEACHER_PASSWORD", "prof123"),
            "nombre": "Profesor",
            "apellido": "Usuario",
            "rol_name": "profesor",
            "rol_desc": "Docente de la institución",
        },
        {
            "email": os.getenv("TEST_PARENT_EMAIL", "padre@colegio.edu"),
            "password": os.getenv("TEST_PARENT_PASSWORD", "papa123"),
            "nombre": "Acudiente",
            "apellido": "Usuario",
            "rol_name": "acudiente",
            "rol_desc": "Acudiente de estudiante",
        },
    ]
    
    try:
        with uow() as unit_of_work:
            # Crear o obtener roles
            print("\n[*] Verificando/creando roles...")
            roles = {}
            for user_data in test_users:
                rol_name = user_data["rol_name"]
                if rol_name not in roles:
                    roles[rol_name] = get_or_create_role(
                        unit_of_work,
                        rol_name,
                        user_data["rol_desc"]
                    )
                    print(f"    ✓ Rol '{rol_name}' OK")
            
            unit_of_work.commit()
            
            # Crear usuarios
            print("\n[*] Verificando/creando usuarios de prueba...")
            for user_data in test_users:
                email = user_data["email"]
                
                # Verificar si usuario ya existe
                existing_user = unit_of_work.usuarios.get_by_email(email)
                if existing_user:
                    print(f"    ℹ Usuario {email} ya existe (saltando)")
                    continue
                
                # Crear Persona
                persona = Persona(
                    numero_identificacion=f"TEST{hash(email) % 10000:04d}",
                    tipo_identificacion="CC",
                    primer_nombre=user_data["nombre"],
                    primer_apellido=user_data["apellido"],
                    segundo_nombre="",
                    segundo_apellido="",
                    fecha_nacimiento=datetime(1990, 1, 1),
                    telefono="",
                    direccion="",
                    genero="",
                    type="Usuario"
                )
                
                # Crear Usuario
                usuario = Usuario(
                    correo_electronico=email,
                    contrasena=user_data["password"],  # ⚠️ En producción: bcrypt
                    id_rol=roles[user_data["rol_name"]].id_rol,
                    activo=True,
                    fecha_creacion=datetime.now(),
                    ultimo_ingreso=None
                )
                usuario.persona = persona
                
                unit_of_work.usuarios.add(usuario)
                print(f"    ✓ Usuario {email} creado correctamente")
            
            unit_of_work.commit()
            print("\n" + "=" * 70)
            print("✓ Usuarios de prueba insertados correctamente")
            print("=" * 70)
            
            # Mostrar credenciales
            print("\n[*] Credenciales de prueba (desde .env):\n")
            for user_data in test_users:
                print(f"    Email: {user_data['email']}")
                print(f"    Contraseña: {user_data['password']}")
                print(f"    Rol: {user_data['rol_name']}")
                print()
            
            print("=" * 70)
            print("⚠️  IMPORTANTE PARA PRODUCCIÓN:")
            print("   1. Cambiar ENVIRONMENT=production en .env")
            print("   2. Usar bcrypt para hashear contraseñas")
            print("   3. Eliminar credenciales de prueba de .env")
            print("=" * 70)
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    insert_test_users()
