#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/create_test_users.py

Script para crear usuarios de prueba con la arquitectura correcta:
- Administrador hereda de Usuario (SQL directo)
- Profesor/Directivo/Acudiente heredan de Persona con FK a Usuario

Uso:
    python scripts/create_test_users.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Configurar salida UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.data.db import engine
from sqlalchemy import text
import bcrypt

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_users():
    """Crea usuarios usando la arquitectura correcta"""
    
    print("=" * 70)
    print("CREANDO USUARIOS DE PRUEBA")
    print("=" * 70)
    
    test_users = [
        {
            "email": "admin@colegio.edu",
            "password": "admin123",
            "nombre": "Admin",
            "apellido": "Sistema",
            "rol_id": 1,
            "rol_name": "administrador",
        },
        {
            "email": "director@colegio.edu",
            "password": "dir123",
            "nombre": "Director",
            "apellido": "General",
            "rol_id": 2,
            "rol_name": "director",
        },
        {
            "email": "profesor@colegio.edu",
            "password": "prof123",
            "nombre": "Profesor",
            "apellido": "Ejemplo",
            "rol_id": 3,
            "rol_name": "profesor",
        },
        {
            "email": "padre@colegio.edu",
            "password": "papa123",
            "nombre": "Padre",
            "apellido": "Familia",
            "rol_id": 4,
            "rol_name": "acudiente",
        },
    ]
    
    try:
        with engine.connect() as conn:
            print("\n[*] Creando usuarios...")
            
            for user_data in test_users:
                email = user_data["email"]
                rol_name = user_data["rol_name"]
                
                # Verificar si usuario existe
                result = conn.execute(
                    text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                    {"email": email}
                )
                existing = result.scalar()
                
                if existing:
                    print(f"    [i] {email}: ya existe")
                    continue
                
                if rol_name == "administrador":
                    # ADMINISTRADOR: hereda de Usuario (Joined Table Inheritance)
                    # Primero insertar en Usuario con contraseña hasheada
                    hashed_password = hash_password(user_data["password"])
                    result = conn.execute(
                        text("""
                            INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo, fecha_creacion)
                            VALUES (:email, :password, :rol_id, true, :fecha)
                            RETURNING id_usuario
                        """),
                        {
                            "email": email,
                            "password": hashed_password,
                            "rol_id": user_data["rol_id"],
                            "fecha": datetime.now()
                        }
                    )
                    user_id = result.scalar()
                    
                    # Luego insertar en Administrador (hereda de Usuario)
                    conn.execute(
                        text("""
                            INSERT INTO administrador (id_administrador, primer_nombre, primer_apellido, telefono)
                            VALUES (:user_id, :nombre, :apellido, '')
                        """),
                        {
                            "user_id": user_id,
                            "nombre": user_data["nombre"],
                            "apellido": user_data["apellido"]
                        }
                    )
                    conn.commit()
                    print(f"    [OK] {email} (Administrador, id={user_id})")
                
                else:
                    # OTROS ROLES: Persona + Usuario asociado
                    # Primero crear Usuario con contraseña hasheada
                    hashed_password = hash_password(user_data["password"])
                    result = conn.execute(
                        text("""
                            INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo, fecha_creacion)
                            VALUES (:email, :password, :rol_id, true, :fecha)
                            RETURNING id_usuario
                        """),
                        {
                            "email": email,
                            "password": hashed_password,
                            "rol_id": user_data["rol_id"],
                            "fecha": datetime.now()
                        }
                    )
                    user_id = result.scalar()
                    
                    # Crear Persona
                    result = conn.execute(
                        text("""
                            INSERT INTO persona (tipo_identificacion, numero_identificacion, 
                                               primer_nombre, primer_apellido, fecha_nacimiento, type)
                            VALUES ('CC', :num_id, :nombre, :apellido, '1990-01-01'::date, :tipo)
                            RETURNING id_persona
                        """),
                        {
                            "num_id": f"TEST{user_id:04d}",
                            "nombre": user_data["nombre"],
                            "apellido": user_data["apellido"],
                            "tipo": rol_name if rol_name != "acudiente" else "acudiente"
                        }
                    )
                    persona_id = result.scalar()
                    
                    # Crear rol específico con FK a Usuario
                    if rol_name == "director":
                        conn.execute(
                            text("""
                                INSERT INTO directivo (id_directivo, id_usuario, cargo, area_responsable)
                                VALUES (:persona_id, :user_id, 'Director General', 'Dirección')
                            """),
                            {"persona_id": persona_id, "user_id": user_id}
                        )
                    elif rol_name == "profesor":
                        conn.execute(
                            text("""
                                INSERT INTO profesor (id_profesor, id_usuario, especialidad, experiencia_anios)
                                VALUES (:persona_id, :user_id, 'Generalista', 5)
                            """),
                            {"persona_id": persona_id, "user_id": user_id}
                        )
                    elif rol_name == "acudiente":
                        conn.execute(
                            text("""
                                INSERT INTO acudiente (id_acudiente, id_usuario, parentesco)
                                VALUES (:persona_id, :user_id, 'Padre')
                            """),
                            {"persona_id": persona_id, "user_id": user_id}
                        )
                    
                    conn.commit()
                    print(f"    [OK] {email} ({rol_name.capitalize()}, user_id={user_id}, persona_id={persona_id})")
            
            print("\n" + "=" * 70)
            print("[OK] Usuarios creados exitosamente")
            print("=" * 70)
            
            print("\n[*] Credenciales de prueba:\n")
            for user_data in test_users:
                print(f"    Email: {user_data['email']}")
                print(f"    Contraseña: {user_data['password']}")
                print(f"    Rol: {user_data['rol_name']}")
                print()
    
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    create_users()
