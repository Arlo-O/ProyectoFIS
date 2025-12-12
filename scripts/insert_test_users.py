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
from sqlalchemy import select

# Agregar la ruta del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.data.uow import uow
from app.core.usuarios.persona import Persona
from app.core.usuarios.usuario import Usuario
from app.core.usuarios.administrador import Administrador
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.acudiente import Acudiente
from app.core.usuarios.rol import Rol

# ✅ Inicializar los mapeos de SQLAlchemy
from app.data.mappers import start_mappers
start_mappers()


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
    stmt = select(Rol).where(Rol.nombre_rol == role_name)
    role = unit_of_work.session.execute(stmt).scalar_one_or_none()
    if not role:
        role = Rol(nombre_rol=role_name, descripcion_rol=description)
        unit_of_work.session.add(role)
        unit_of_work.session.flush()  # Flush para obtener el id_rol generado
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
                    try:
                        roles[rol_name] = get_or_create_role(
                            unit_of_work,
                            rol_name,
                            user_data["rol_desc"]
                        )
                        print(f"    ✓ Rol '{rol_name}' OK")
                    except Exception as e:
                        # Rol ya existe, obtenerlo
                        stmt = select(Rol).where(Rol.nombre_rol == rol_name)
                        roles[rol_name] = unit_of_work.session.execute(stmt).scalar_one_or_none()
                        if roles[rol_name]:
                            print(f"    ✓ Rol '{rol_name}' ya existe")
                            unit_of_work.session.rollback()
                        else:
                            raise
            
            try:
                unit_of_work.commit()
            except Exception:
                # Si hay error al hacer commit (roles duplicados), solo hacer rollback
                unit_of_work.session.rollback()
            
            # Crear usuarios
            print("\n[*] Verificando/creando usuarios de prueba...")
            for user_data in test_users:
                email = user_data["email"]
                
                # Verificar si usuario ya existe
                existing_user = unit_of_work.usuarios.get_by_email(email)
                if existing_user:
                    print(f"    ℹ Usuario {email} ya existe (saltando)")
                    continue
                
                rol_name = user_data["rol_name"]
                rol = roles.get(rol_name)
                if not rol:
                    # Obtener el rol de la BD si no lo encontramos
                    stmt = select(Rol).where(Rol.nombre_rol == rol_name)
                    rol = unit_of_work.session.execute(stmt).scalar_one_or_none()
                    if not rol:
                        print(f"    ✗ Rol {rol_name} no encontrado")
                        continue
                    roles[rol_name] = rol
                
                # Crear Usuario
                usuario = Usuario(
                    id_usuario=None,  # Será asignado por la BD
                    correo_electronico=email,
                    contrasena=user_data["password"],  # ⚠️ En producción: bcrypt
                    id_rol=rol.id_rol,
                    activo=True,
                    fecha_creacion=datetime.now(),
                    ultimo_ingreso=None
                )
                
                unit_of_work.usuarios.add(usuario)
                unit_of_work.session.flush()  # Flush para obtener el id_usuario generado
                
                # Crear la entidad de rol específica (Persona) con FK a Usuario
                if rol_name == "administrador":
                    persona = Administrador(
                        id_administrador=None,
                        id_persona=None,
                        tipo_identificacion="CC",
                        numero_identificacion=f"TEST{hash(email) % 10000:04d}",
                        primer_nombre=user_data["nombre"],
                        segundo_nombre="",
                        primer_apellido=user_data["apellido"],
                        segundo_apellido="",
                        fecha_nacimiento=datetime(1990, 1, 1),
                        telefono="",
                        direccion="",
                        genero="",
                    )
                    persona.usuario = usuario
                    unit_of_work.session.add(persona)
                    
                elif rol_name == "director":
                    persona = Directivo(
                        id_directivo=None,
                        id_persona=None,
                        cargo="Director",
                        area_responsable="Dirección",
                        tipo_identificacion="CC",
                        numero_identificacion=f"TEST{hash(email) % 10000:04d}",
                        primer_nombre=user_data["nombre"],
                        segundo_nombre="",
                        primer_apellido=user_data["apellido"],
                        segundo_apellido="",
                        fecha_nacimiento=datetime(1990, 1, 1),
                        telefono="",
                        direccion="",
                        genero="",
                    )
                    persona.usuario = usuario
                    unit_of_work.session.add(persona)
                    
                elif rol_name == "profesor":
                    persona = Profesor(
                        id_profesor=None,
                        id_persona=None,
                        especialidad="Generalista",
                        experiencia_anios=5,
                        tipo_identificacion="CC",
                        numero_identificacion=f"TEST{hash(email) % 10000:04d}",
                        primer_nombre=user_data["nombre"],
                        segundo_nombre="",
                        primer_apellido=user_data["apellido"],
                        segundo_apellido="",
                        fecha_nacimiento=datetime(1990, 1, 1),
                        telefono="",
                        direccion="",
                        genero="",
                    )
                    persona.usuario = usuario
                    unit_of_work.session.add(persona)
                    
                elif rol_name == "acudiente":
                    persona = Acudiente(
                        id_acudiente=None,
                        id_persona=None,
                        parentesco="Padre",
                        tipo_identificacion="CC",
                        numero_identificacion=f"TEST{hash(email) % 10000:04d}",
                        primer_nombre=user_data["nombre"],
                        segundo_nombre="",
                        primer_apellido=user_data["apellido"],
                        segundo_apellido="",
                        fecha_nacimiento=datetime(1990, 1, 1),
                        telefono="",
                        direccion="",
                        genero="",
                    )
                    persona.usuario = usuario
                    unit_of_work.session.add(persona)
                
                print(f"    ✓ Usuario {email} ({rol_name}) creado correctamente")
            
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
