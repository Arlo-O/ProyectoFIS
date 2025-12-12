"""
initial_data.py - Insertar Datos Iniciales de Prueba

Script para insertar roles y usuarios de prueba en la base de datos.

Ejecutar UNA SOLA VEZ después de crear las tablas:
    python app/config/initial_data.py

Los datos se obtienen de las variables de entorno en .env
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Agregar ruta raíz
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.data.uow import uow
from app.core.usuarios.rol import Rol
from app.core.usuarios.persona import Persona
from app.core.usuarios.usuario import Usuario
from app.core.usuarios.administrador import Administrador
from app.core.usuarios.directivo import Directivo
from app.core.usuarios.profesor import Profesor
from app.core.usuarios.estudiante import Estudiante
from app.config.settings import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD,
    TEST_DIRECTOR_EMAIL, TEST_DIRECTOR_PASSWORD,
    TEST_TEACHER_EMAIL, TEST_TEACHER_PASSWORD,
    TEST_STUDENT_EMAIL, TEST_STUDENT_PASSWORD
)

import bcrypt


def hash_password(password: str) -> str:
    """Hashear contraseña con bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def insert_roles():
    """Inserta los roles base del sistema."""
    print("\n[*] Insertando roles...")
    
    with uow() as unit:
        roles_data = [
            ("ADMINISTRADOR", "Acceso total al sistema"),
            ("DIRECTOR", "Gestión académica y administrativa"),
            ("PROFESOR", "Gestión de calificaciones y estudiantes"),
            ("ESTUDIANTE", "Visualización de calificaciones y información académica"),
            ("ACUDIENTE", "Visualización del desempeño de su estudiante"),
        ]
        
        for nombre, descripcion in roles_data:
            # Verificar si el rol ya existe
            existing_role = unit.session.query(Rol).filter_by(nombre_rol=nombre).first()
            if existing_role:
                print(f"  [·] Rol '{nombre}' ya existe")
                continue
            
            role = Rol(nombre_rol=nombre, descripcion_rol=descripcion)
            unit.session.add(role)
            print(f"  [✓] Rol '{nombre}' creado")
        
        unit.session.commit()


def insert_test_admin():
    """Inserta usuario administrador de prueba."""
    print("\n[*] Insertando administrador de prueba...")
    
    with uow() as unit:
        # Verificar si ya existe
        existing = unit.session.query(Usuario).filter_by(
            correo_electronico=TEST_ADMIN_EMAIL
        ).first()
        
        if existing:
            print(f"  [·] Admin '{TEST_ADMIN_EMAIL}' ya existe")
            return
        
        # Obtener rol
        rol_admin = unit.session.query(Rol).filter_by(nombre_rol="ADMINISTRADOR").first()
        if not rol_admin:
            print("  [!] Rol ADMINISTRADOR no encontrado")
            return
        
        # Crear persona
        persona = Persona(
            tipo_identificacion="CC",
            numero_identificacion="123456789",
            primer_nombre="Admin",
            primer_apellido="Sistema",
            fecha_nacimiento=datetime(1990, 1, 1),
            genero="M",
            direccion="Calle Principal 123",
            telefono="3001234567"
        )
        unit.session.add(persona)
        unit.session.flush()  # Obtener ID de persona
        
        # Crear administrador
        admin = Administrador(
            id_administrador=None,
            id_usuario=None,
            correo_electronico=TEST_ADMIN_EMAIL,
            contrasena=hash_password(TEST_ADMIN_PASSWORD),
            id_rol=rol_admin.id_rol,
            activo=True,
            id_persona=persona.id_persona,
            tipo_identificacion="CC",
            numero_identificacion="123456789",
            primer_nombre="Admin",
            primer_apellido="Sistema",
            fecha_nacimiento=datetime(1990, 1, 1),
            genero="M",
            direccion="Calle Principal 123",
            telefono="3001234567"
        )
        unit.session.add(admin)
        unit.session.commit()
        
        print(f"  [✓] Admin '{TEST_ADMIN_EMAIL}' creado (contraseña: {TEST_ADMIN_PASSWORD})")


def insert_test_users():
    """Inserta usuarios de prueba para cada rol."""
    print("\n[*] Insertando usuarios de prueba...")
    
    test_users = [
        (TEST_DIRECTOR_EMAIL, TEST_DIRECTOR_PASSWORD, "DIRECTOR", "Director", "Académico"),
        (TEST_TEACHER_EMAIL, TEST_TEACHER_PASSWORD, "PROFESOR", "Profesor", "Matemáticas"),
        (TEST_STUDENT_EMAIL, TEST_STUDENT_PASSWORD, "ESTUDIANTE", "Estudiante", "Test"),
    ]
    
    with uow() as unit:
        for email, password, rol_nombre, nombre, apellido in test_users:
            # Verificar si ya existe
            existing = unit.session.query(Usuario).filter_by(
                correo_electronico=email
            ).first()
            
            if existing:
                print(f"  [·] Usuario '{email}' ya existe")
                continue
            
            # Obtener rol
            rol = unit.session.query(Rol).filter_by(nombre_rol=rol_nombre).first()
            if not rol:
                print(f"  [!] Rol '{rol_nombre}' no encontrado")
                continue
            
            # Crear persona base
            persona = Persona(
                tipo_identificacion="CC",
                numero_identificacion=f"1000{len(email)}",
                primer_nombre=nombre,
                primer_apellido=apellido,
                fecha_nacimiento=datetime(1990, 1, 1),
                genero="M",
                direccion="Calle Test 123",
                telefono="3001234567"
            )
            unit.session.add(persona)
            unit.session.flush()
            
            # Crear usuario específico según rol
            if rol_nombre == "DIRECTOR":
                usuario = Directivo(
                    id_directivo=None,
                    id_usuario=None,
                    correo_electronico=email,
                    contrasena=hash_password(password),
                    id_rol=rol.id_rol,
                    activo=True,
                    id_persona=persona.id_persona,
                    tipo_identificacion="CC",
                    numero_identificacion=f"1000{len(email)}",
                    primer_nombre=nombre,
                    primer_apellido=apellido,
                )
            elif rol_nombre == "PROFESOR":
                usuario = Profesor(
                    id_profesor=None,
                    id_usuario=None,
                    correo_electronico=email,
                    contrasena=hash_password(password),
                    id_rol=rol.id_rol,
                    activo=True,
                    id_persona=persona.id_persona,
                    tipo_identificacion="CC",
                    numero_identificacion=f"1000{len(email)}",
                    primer_nombre=nombre,
                    primer_apellido=apellido,
                    especialidad=apellido,
                    experiencia_anios=5
                )
            elif rol_nombre == "ESTUDIANTE":
                usuario = Estudiante(
                    id_estudiante=None,
                    id_usuario=None,
                    correo_electronico=email,
                    contrasena=hash_password(password),
                    id_rol=rol.id_rol,
                    activo=True,
                    id_persona=persona.id_persona,
                    tipo_identificacion="CC",
                    numero_identificacion=f"1000{len(email)}",
                    primer_nombre=nombre,
                    primer_apellido=apellido,
                    codigo_matricula=f"EST{len(email):04d}",
                    fecha_ingreso=datetime.now()
                )
            else:
                usuario = Usuario(
                    id_usuario=None,
                    correo_electronico=email,
                    contrasena=hash_password(password),
                    id_rol=rol.id_rol,
                    activo=True,
                    id_persona=persona.id_persona,
                    tipo_identificacion="CC",
                    numero_identificacion=f"1000{len(email)}",
                    primer_nombre=nombre,
                    primer_apellido=apellido,
                )
            
            unit.session.add(usuario)
            unit.session.commit()
            print(f"  [✓] {rol_nombre.capitalize()} '{email}' creado (contraseña: {password})")


def initialize_data():
    """Función principal para insertar datos iniciales."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "INICIALIZADOR DE DATOS DE PRUEBA" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        insert_roles()
        insert_test_admin()
        insert_test_users()
        
        print("\n" + "=" * 70)
        print("[✓] DATOS INICIALES INSERTADOS EXITOSAMENTE")
        print("=" * 70)
        print("\nCuentas de prueba creadas:")
        print(f"  Admin:     {TEST_ADMIN_EMAIL} / {TEST_ADMIN_PASSWORD}")
        print(f"  Director:  {TEST_DIRECTOR_EMAIL} / {TEST_DIRECTOR_PASSWORD}")
        print(f"  Profesor:  {TEST_TEACHER_EMAIL} / {TEST_TEACHER_PASSWORD}")
        print(f"  Estudiante: {TEST_STUDENT_EMAIL} / {TEST_STUDENT_PASSWORD}")
        print("\nPuedes iniciar la aplicación: python run_app.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n[✗] Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    initialize_data()
