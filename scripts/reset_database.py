#!/usr/bin/env python
"""
scripts/reset_database.py

Script para limpiar y recrear la base de datos desde cero.
Ejecuta ALEMBIC para aplicar todas las migraciones o crea tablas manualmente.

Uso:
    python scripts/reset_database.py
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Agregar la ruta del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

# Importar la BD y los mappers
from app.data.db import engine
from app.data.mappers import start_mappers, metadata
from sqlalchemy import text, inspect


def get_db_connection():
    """Obtiene conexión directa a PostgreSQL (sin SQLAlchemy)"""
    try:
        db_url = os.getenv("DATABASE_URL")
        # Parsear la URL: postgresql+psycopg2://user:password@host:port/dbname
        parts = db_url.split("://")[1].split("@")
        user_pass = parts[0].split(":")
        host_db = parts[1].split("/")
        
        conn = psycopg2.connect(
            host=host_db[0].split(":")[0],
            port=int(host_db[0].split(":")[1]) if ":" in host_db[0] else 5432,
            user=user_pass[0],
            password=user_pass[1],
            database=host_db[1]
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la BD: {e}")
        return None


def drop_all_tables():
    """Elimina todas las tablas de la BD"""
    print("\n[*] Eliminando todas las tablas...")
    try:
        with engine.connect() as conn:
            # Deshabilitar constraints temporalmente
            conn.execute(text("SET session_replication_role = 'replica'"))
            
            # Obtener todas las tablas
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if not tables:
                print("    ℹ️  No hay tablas para eliminar")
                return
            
            # Eliminar cada tabla
            for table in tables:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"    ✓ Tabla '{table}' eliminada")
                except Exception as e:
                    print(f"    ⚠️  Error eliminando '{table}': {e}")
            
            # Reabilitar constraints
            conn.execute(text("SET session_replication_role = 'origin'"))
            conn.commit()
            
        print("    ✓ Todas las tablas eliminadas")
    except Exception as e:
        print(f"    ❌ Error: {e}")
        import traceback
        traceback.print_exc()


def create_all_tables():
    """Crea todas las tablas desde los mappers"""
    print("\n[*] Creando tablas...")
    try:
        # Inicializar mappers
        start_mappers()
        
        # Crear todas las tablas desde metadata
        metadata.create_all(bind=engine)
        
        print("    ✓ Todas las tablas creadas exitosamente")
    except Exception as e:
        print(f"    ❌ Error: {e}")
        import traceback
        traceback.print_exc()


def seed_initial_data():
    """Inserta datos iniciales: roles y permisos"""
    print("\n[*] Insertando datos iniciales...")
    try:
        from app.data.uow import uow
        from app.core.usuarios.rol import Rol
        from app.core.usuarios.permiso import Permiso
        from sqlalchemy import select
        
        with uow() as unit_of_work:
            # Crear roles
            roles_data = [
                ("administrador", "Administrador del sistema con acceso total"),
                ("director", "Director de la institución"),
                ("profesor", "Docente de la institución"),
                ("acudiente", "Acudiente o padre de familia"),
                ("aspirante", "Aspirante a la institución"),
            ]
            
            roles = {}
            for nombre, descripcion in roles_data:
                # Verificar que no exista
                stmt = select(Rol).where(Rol.nombre_rol == nombre)
                existing = unit_of_work.session.execute(stmt).scalar_one_or_none()
                
                if not existing:
                    rol = Rol(nombre_rol=nombre, descripcion_rol=descripcion)
                    unit_of_work.session.add(rol)
                    roles[nombre] = rol
                    print(f"    ✓ Rol '{nombre}' creado")
                else:
                    roles[nombre] = existing
                    print(f"    ℹ️  Rol '{nombre}' ya existe")
            
            unit_of_work.commit()
            
            # Crear permisos básicos
            permisos_data = [
                ("crear_usuario", "Crear nuevos usuarios"),
                ("editar_usuario", "Editar información de usuarios"),
                ("eliminar_usuario", "Eliminar usuarios"),
                ("ver_estudiantes", "Ver información de estudiantes"),
                ("ver_boletines", "Ver boletines académicos"),
                ("crear_logro", "Crear logros educativos"),
                ("evaluar_logro", "Evaluar logros de estudiantes"),
                ("crear_citacion", "Crear citaciones a acudientes"),
                ("ver_entrevistas", "Ver entrevistas de aspirantes"),
            ]
            
            permisos = {}
            for nombre, descripcion in permisos_data:
                stmt = select(Permiso).where(Permiso.nombre == nombre)
                existing = unit_of_work.session.execute(stmt).scalar_one_or_none()
                
                if not existing:
                    permiso = Permiso(nombre=nombre, descripcion=descripcion)
                    unit_of_work.session.add(permiso)
                    permisos[nombre] = permiso
                    print(f"    ✓ Permiso '{nombre}' creado")
                else:
                    permisos[nombre] = existing
                    print(f"    ℹ️  Permiso '{nombre}' ya existe")
            
            unit_of_work.commit()
            
            # Asignar permisos a roles (ejemplo para administrador)
            admin_role = roles.get("administrador")
            if admin_role:
                # El administrador tiene acceso a todo
                for permiso in permisos.values():
                    if permiso not in admin_role.permisos:
                        admin_role.permisos.append(permiso)
                unit_of_work.commit()
                print(f"    ✓ Permisos asignados a administrador")
        
        print("    ✓ Datos iniciales insertados")
    except Exception as e:
        print(f"    ❌ Error: {e}")
        import traceback
        traceback.print_exc()


def reset_database():
    """Flujo completo de reset"""
    print("=" * 70)
    print("🔧 RESET COMPLETO DE BASE DE DATOS")
    print("=" * 70)
    
    # Paso 1: Eliminar tablas
    drop_all_tables()
    
    # Paso 2: Crear tablas
    create_all_tables()
    
    # Paso 3: Insertar datos iniciales
    seed_initial_data()
    
    print("\n" + "=" * 70)
    print("✅ Base de datos reseteada exitosamente")
    print("=" * 70)
    print("\n[*] Próximos pasos:")
    print("    1. Ejecutar: python scripts/insert_test_users.py")
    print("       (Para crear usuarios de prueba)")
    print("    2. Ejecutar: python seed_permisos.py")
    print("       (Para crear permisos adicionales si es necesario)")
    print("    3. Ejecutar: python run_app.py")
    print("       (Para iniciar la aplicación)")
    print("=" * 70)


if __name__ == "__main__":
    try:
        reset_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
