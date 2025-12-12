#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/populate_database.py

Script para poblar la base de datos con datos de prueba completos:
- Administradores
- Profesores con usuarios
- Directivos con usuarios
- Acudientes con usuarios
- Estudiantes (sin usuario)
- Aspirantes con formularios de preinscripción

Uso:
    python scripts/populate_database.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json

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

def guardar_credenciales(credenciales_list):
    """Guarda las credenciales en el archivo de logs"""
    log_path = project_root / "logs" / "credenciales_usuarios.txt"
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CREDENCIALES DE USUARIOS - DATOS DE PRUEBA\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        for cred in credenciales_list:
            f.write(f"Rol: {cred['rol']}\n")
            f.write(f"Nombre: {cred['nombre']}\n")
            f.write(f"Email: {cred['email']}\n")
            f.write(f"Contraseña: {cred['password']}\n")
            if 'cedula' in cred:
                f.write(f"Cédula: {cred['cedula']}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"\n✅ Credenciales guardadas en: {log_path}")

def populate_database():
    """Puebla la base de datos con datos completos"""
    
    print("=" * 80)
    print("POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 80)
    
    credenciales = []
    
    with engine.connect() as conn:
        trans = conn.begin()
        
        try:
            # ==================== ROLES ====================
            print("\n📋 Verificando roles...")
            roles = {
                'administrador': None,
                'profesor': None,
                'directivo': None,
                'acudiente': None
            }
            
            for rol_nombre in roles.keys():
                result = conn.execute(
                    text("SELECT id_rol FROM rol WHERE nombre_rol = :nombre"),
                    {"nombre": rol_nombre}
                ).fetchone()
                
                if result:
                    roles[rol_nombre] = result[0]
                    print(f"  ✓ Rol '{rol_nombre}' encontrado: ID {result[0]}")
                else:
                    result = conn.execute(
                        text("INSERT INTO rol (nombre_rol) VALUES (:nombre) RETURNING id_rol"),
                        {"nombre": rol_nombre}
                    ).fetchone()
                    roles[rol_nombre] = result[0]
                    print(f"  ✓ Rol '{rol_nombre}' creado: ID {result[0]}")
            
            # ==================== ADMINISTRADORES ====================
            print("\n👤 Creando administradores...")
            admins = [
                {
                    "email": "admin@colegio.edu",
                    "password": "admin123",
                    "primer_nombre": "Carlos",
                    "segundo_nombre": "Alberto",
                    "primer_apellido": "Ramírez",
                    "segundo_apellido": "Torres",
                    "telefono": "3001234567"
                },
                {
                    "email": "admin2@colegio.edu",
                    "password": "admin456",
                    "primer_nombre": "María",
                    "segundo_nombre": "Fernanda",
                    "primer_apellido": "González",
                    "segundo_apellido": "López",
                    "telefono": "3009876543"
                }
            ]
            
            for admin in admins:
                # Verificar si existe
                existe = conn.execute(
                    text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                    {"email": admin['email']}
                ).fetchone()
                
                if existe:
                    print(f"  ⚠️  Administrador {admin['email']} ya existe")
                    continue
                
                # Crear usuario
                id_usuario = conn.execute(
                    text("""
                        INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                        VALUES (:email, :pwd, :rol, true)
                        RETURNING id_usuario
                    """),
                    {
                        "email": admin['email'],
                        "pwd": hash_password(admin['password']),
                        "rol": roles['administrador']
                    }
                ).fetchone()[0]
                
                # Crear administrador
                conn.execute(
                    text("""
                        INSERT INTO administrador (id_administrador, primer_nombre, segundo_nombre, 
                                                  primer_apellido, segundo_apellido, telefono)
                        VALUES (:id, :p_nombre, :s_nombre, :p_apellido, :s_apellido, :tel)
                    """),
                    {
                        "id": id_usuario,
                        "p_nombre": admin['primer_nombre'],
                        "s_nombre": admin['segundo_nombre'],
                        "p_apellido": admin['primer_apellido'],
                        "s_apellido": admin['segundo_apellido'],
                        "tel": admin['telefono']
                    }
                )
                
                nombre_completo = f"{admin['primer_nombre']} {admin['segundo_nombre']} {admin['primer_apellido']} {admin['segundo_apellido']}"
                print(f"  ✅ Administrador: {nombre_completo} ({admin['email']})")
                
                credenciales.append({
                    'rol': 'Administrador',
                    'nombre': nombre_completo,
                    'email': admin['email'],
                    'password': admin['password']
                })
            
            # ==================== PROFESORES ====================
            print("\n👨‍🏫 Creando profesores...")
            profesores = [
                {
                    "email": "profesor1@colegio.edu",
                    "password": "prof123",
                    "cedula": "1010101010",
                    "primer_nombre": "Luis",
                    "segundo_nombre": "Felipe",
                    "primer_apellido": "Martínez",
                    "segundo_apellido": "Silva",
                    "fecha_nacimiento": "1985-05-15",
                    "genero": "M",
                    "direccion": "Calle 45 #12-34",
                    "telefono": "3101234567",
                    "especialidad": "Educación Infantil",
                    "experiencia": 8
                },
                {
                    "email": "profesor2@colegio.edu",
                    "password": "prof456",
                    "cedula": "1020202020",
                    "primer_nombre": "Ana",
                    "segundo_nombre": "María",
                    "primer_apellido": "Rodríguez",
                    "segundo_apellido": "Pérez",
                    "fecha_nacimiento": "1990-08-22",
                    "genero": "F",
                    "direccion": "Carrera 20 #8-90",
                    "telefono": "3209876543",
                    "especialidad": "Pedagogía Preescolar",
                    "experiencia": 5
                },
                {
                    "email": "profesor3@colegio.edu",
                    "password": "prof789",
                    "cedula": "1030303030",
                    "primer_nombre": "Jorge",
                    "segundo_nombre": "Andrés",
                    "primer_apellido": "Gómez",
                    "segundo_apellido": "Vargas",
                    "fecha_nacimiento": "1988-03-10",
                    "genero": "M",
                    "direccion": "Calle 67 #23-45",
                    "telefono": "3151234567",
                    "especialidad": "Educación Física",
                    "experiencia": 10
                }
            ]
            
            for prof in profesores:
                # Verificar si existe persona
                existe_persona = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": prof['cedula']}
                ).fetchone()
                
                if existe_persona:
                    print(f"  ⚠️  Profesor con cédula {prof['cedula']} ya existe")
                    continue
                
                # Crear persona
                id_persona = conn.execute(
                    text("""
                        INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                           primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                           fecha_nacimiento, genero, direccion, telefono, type)
                        VALUES ('Cédula', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                :fecha, :genero, :dir, :tel, 'profesor')
                        RETURNING id_persona
                    """),
                    {
                        "cedula": prof['cedula'],
                        "p_nombre": prof['primer_nombre'],
                        "s_nombre": prof['segundo_nombre'],
                        "p_apellido": prof['primer_apellido'],
                        "s_apellido": prof['segundo_apellido'],
                        "fecha": prof['fecha_nacimiento'],
                        "genero": prof['genero'],
                        "dir": prof['direccion'],
                        "tel": prof['telefono']
                    }
                ).fetchone()[0]
                
                # Crear usuario
                id_usuario = conn.execute(
                    text("""
                        INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                        VALUES (:email, :pwd, :rol, true)
                        RETURNING id_usuario
                    """),
                    {
                        "email": prof['email'],
                        "pwd": hash_password(prof['password']),
                        "rol": roles['profesor']
                    }
                ).fetchone()[0]
                
                # Crear profesor
                conn.execute(
                    text("""
                        INSERT INTO profesor (id_profesor, id_usuario, especialidad, experiencia_anios)
                        VALUES (:id_persona, :id_usuario, :esp, :exp)
                    """),
                    {
                        "id_persona": id_persona,
                        "id_usuario": id_usuario,
                        "esp": prof['especialidad'],
                        "exp": prof['experiencia']
                    }
                )
                
                nombre_completo = f"{prof['primer_nombre']} {prof['segundo_nombre']} {prof['primer_apellido']} {prof['segundo_apellido']}"
                print(f"  ✅ Profesor: {nombre_completo} ({prof['email']}) - Cédula: {prof['cedula']}")
                
                credenciales.append({
                    'rol': 'Profesor',
                    'nombre': nombre_completo,
                    'email': prof['email'],
                    'password': prof['password'],
                    'cedula': prof['cedula']
                })
            
            # ==================== DIRECTIVOS ====================
            print("\n👔 Creando directivos...")
            directivos = [
                {
                    "email": "director@colegio.edu",
                    "password": "dir123",
                    "cedula": "1040404040",
                    "primer_nombre": "Patricia",
                    "segundo_nombre": "Elena",
                    "primer_apellido": "Sánchez",
                    "segundo_apellido": "Castro",
                    "fecha_nacimiento": "1975-11-08",
                    "genero": "F",
                    "direccion": "Calle 89 #34-56",
                    "telefono": "3161234567",
                    "cargo": "Directora General",
                    "area": "Dirección Académica"
                },
                {
                    "email": "coordinador@colegio.edu",
                    "password": "coord123",
                    "cedula": "1050505050",
                    "primer_nombre": "Roberto",
                    "segundo_nombre": "Carlos",
                    "primer_apellido": "Mendoza",
                    "segundo_apellido": "Ruiz",
                    "fecha_nacimiento": "1980-06-18",
                    "genero": "M",
                    "direccion": "Carrera 45 #67-89",
                    "telefono": "3179876543",
                    "cargo": "Coordinador Académico",
                    "area": "Coordinación Preescolar"
                }
            ]
            
            for dir_data in directivos:
                # Verificar si existe email
                existe_email = conn.execute(
                    text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                    {"email": dir_data['email']}
                ).fetchone()
                
                if existe_email:
                    print(f"  ⚠️  Directivo {dir_data['email']} ya existe")
                    continue
                
                # Verificar si existe persona
                existe_persona = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": dir_data['cedula']}
                ).fetchone()
                
                if existe_persona:
                    print(f"  ⚠️  Directivo con cédula {dir_data['cedula']} ya existe")
                    continue
                
                # Crear persona
                id_persona = conn.execute(
                    text("""
                        INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                           primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                           fecha_nacimiento, genero, direccion, telefono, type)
                        VALUES ('Cédula', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                :fecha, :genero, :dir, :tel, 'directivo')
                        RETURNING id_persona
                    """),
                    {
                        "cedula": dir_data['cedula'],
                        "p_nombre": dir_data['primer_nombre'],
                        "s_nombre": dir_data['segundo_nombre'],
                        "p_apellido": dir_data['primer_apellido'],
                        "s_apellido": dir_data['segundo_apellido'],
                        "fecha": dir_data['fecha_nacimiento'],
                        "genero": dir_data['genero'],
                        "dir": dir_data['direccion'],
                        "tel": dir_data['telefono']
                    }
                ).fetchone()[0]
                
                # Crear usuario
                id_usuario = conn.execute(
                    text("""
                        INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                        VALUES (:email, :pwd, :rol, true)
                        RETURNING id_usuario
                    """),
                    {
                        "email": dir_data['email'],
                        "pwd": hash_password(dir_data['password']),
                        "rol": roles['directivo']
                    }
                ).fetchone()[0]
                
                # Crear directivo
                conn.execute(
                    text("""
                        INSERT INTO directivo (id_directivo, id_usuario, cargo, area_responsable)
                        VALUES (:id_persona, :id_usuario, :cargo, :area)
                    """),
                    {
                        "id_persona": id_persona,
                        "id_usuario": id_usuario,
                        "cargo": dir_data['cargo'],
                        "area": dir_data['area']
                    }
                )
                
                nombre_completo = f"{dir_data['primer_nombre']} {dir_data['segundo_nombre']} {dir_data['primer_apellido']} {dir_data['segundo_apellido']}"
                print(f"  ✅ Directivo: {nombre_completo} ({dir_data['email']}) - {dir_data['cargo']}")
                
                credenciales.append({
                    'rol': 'Directivo',
                    'nombre': nombre_completo,
                    'email': dir_data['email'],
                    'password': dir_data['password'],
                    'cedula': dir_data['cedula']
                })
            
            # ==================== ACUDIENTES CON USUARIOS ====================
            print("\n👨‍👩‍👧‍👦 Creando acudientes...")
            acudientes = [
                {
                    "email": "acudiente1@gmail.com",
                    "password": "acud123",
                    "cedula": "1060606060",
                    "primer_nombre": "Juan",
                    "segundo_nombre": "Carlos",
                    "primer_apellido": "Pérez",
                    "segundo_apellido": "Moreno",
                    "fecha_nacimiento": "1982-04-12",
                    "genero": "M",
                    "direccion": "Calle 12 #34-56",
                    "telefono": "3201234567",
                    "parentesco": "Padre"
                },
                {
                    "email": "acudiente2@gmail.com",
                    "password": "acud456",
                    "cedula": "1070707070",
                    "primer_nombre": "Sandra",
                    "segundo_nombre": "Milena",
                    "primer_apellido": "López",
                    "segundo_apellido": "Díaz",
                    "fecha_nacimiento": "1985-09-25",
                    "genero": "F",
                    "direccion": "Carrera 15 #45-67",
                    "telefono": "3159876543",
                    "parentesco": "Madre"
                },
                {
                    "email": "acudiente3@gmail.com",
                    "password": "acud789",
                    "cedula": "1080808080",
                    "primer_nombre": "Diego",
                    "segundo_nombre": "Alejandro",
                    "primer_apellido": "Ramírez",
                    "segundo_apellido": "Ortiz",
                    "fecha_nacimiento": "1980-12-05",
                    "genero": "M",
                    "direccion": "Calle 78 #23-45",
                    "telefono": "3189876543",
                    "parentesco": "Padre"
                }
            ]
            
            acudientes_ids = []
            
            for acud in acudientes:
                # Verificar si existe email
                existe_email = conn.execute(
                    text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                    {"email": acud['email']}
                ).fetchone()
                
                if existe_email:
                    print(f"  ⚠️  Acudiente {acud['email']} ya existe")
                    # Buscar el id_persona asociado
                    existe_persona = conn.execute(
                        text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                        {"cedula": acud['cedula']}
                    ).fetchone()
                    if existe_persona:
                        acudientes_ids.append(existe_persona[0])
                    continue
                
                # Verificar si existe persona
                existe_persona = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": acud['cedula']}
                ).fetchone()
                
                if existe_persona:
                    print(f"  ⚠️  Acudiente con cédula {acud['cedula']} ya existe")
                    acudientes_ids.append(existe_persona[0])
                    continue
                
                # Crear persona
                id_persona = conn.execute(
                    text("""
                        INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                           primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                           fecha_nacimiento, genero, direccion, telefono, type)
                        VALUES ('Cédula', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                :fecha, :genero, :dir, :tel, 'acudiente')
                        RETURNING id_persona
                    """),
                    {
                        "cedula": acud['cedula'],
                        "p_nombre": acud['primer_nombre'],
                        "s_nombre": acud['segundo_nombre'],
                        "p_apellido": acud['primer_apellido'],
                        "s_apellido": acud['segundo_apellido'],
                        "fecha": acud['fecha_nacimiento'],
                        "genero": acud['genero'],
                        "dir": acud['direccion'],
                        "tel": acud['telefono']
                    }
                ).fetchone()[0]
                
                acudientes_ids.append(id_persona)
                
                # Crear usuario
                id_usuario = conn.execute(
                    text("""
                        INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                        VALUES (:email, :pwd, :rol, true)
                        RETURNING id_usuario
                    """),
                    {
                        "email": acud['email'],
                        "pwd": hash_password(acud['password']),
                        "rol": roles['acudiente']
                    }
                ).fetchone()[0]
                
                # Crear acudiente
                conn.execute(
                    text("""
                        INSERT INTO acudiente (id_acudiente, id_usuario, parentesco)
                        VALUES (:id_persona, :id_usuario, :parentesco)
                    """),
                    {
                        "id_persona": id_persona,
                        "id_usuario": id_usuario,
                        "parentesco": acud['parentesco']
                    }
                )
                
                nombre_completo = f"{acud['primer_nombre']} {acud['segundo_nombre']} {acud['primer_apellido']} {acud['segundo_apellido']}"
                print(f"  ✅ Acudiente: {nombre_completo} ({acud['email']}) - {acud['parentesco']}")
                
                credenciales.append({
                    'rol': 'Acudiente',
                    'nombre': nombre_completo,
                    'email': acud['email'],
                    'password': acud['password'],
                    'cedula': acud['cedula']
                })
            
            # ==================== ESTUDIANTES ====================
            print("\n👶 Creando estudiantes...")
            estudiantes = [
                {
                    "cedula": "RC-2020001",
                    "primer_nombre": "Sofía",
                    "segundo_nombre": "Valentina",
                    "primer_apellido": "Pérez",
                    "segundo_apellido": "Moreno",
                    "fecha_nacimiento": "2020-03-15",
                    "genero": "F",
                    "direccion": "Calle 12 #34-56",
                    "telefono": "3201234567",
                    "grado": "Parvulos",
                    "codigo": "EST-2025-001"
                },
                {
                    "cedula": "RC-2019001",
                    "primer_nombre": "Mateo",
                    "segundo_nombre": "Andrés",
                    "primer_apellido": "López",
                    "segundo_apellido": "Díaz",
                    "fecha_nacimiento": "2019-07-22",
                    "genero": "M",
                    "direccion": "Carrera 15 #45-67",
                    "telefono": "3159876543",
                    "grado": "Caminadores",
                    "codigo": "EST-2025-002"
                },
                {
                    "cedula": "RC-2020002",
                    "primer_nombre": "Isabella",
                    "segundo_nombre": "María",
                    "primer_apellido": "Ramírez",
                    "segundo_apellido": "Ortiz",
                    "fecha_nacimiento": "2020-11-08",
                    "genero": "F",
                    "direccion": "Calle 78 #23-45",
                    "telefono": "3189876543",
                    "grado": "Parvulos",
                    "codigo": "EST-2025-003"
                },
                {
                    "cedula": "RC-2018001",
                    "primer_nombre": "Samuel",
                    "segundo_nombre": "David",
                    "primer_apellido": "García",
                    "segundo_apellido": "Torres",
                    "fecha_nacimiento": "2018-05-30",
                    "genero": "M",
                    "direccion": "Carrera 34 #56-78",
                    "telefono": "3167894561",
                    "grado": "Prejardin",
                    "codigo": "EST-2025-004"
                }
            ]
            
            for est in estudiantes:
                # Verificar si existe persona
                existe_persona = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": est['cedula']}
                ).fetchone()
                
                if existe_persona:
                    print(f"  ⚠️  Estudiante con documento {est['cedula']} ya existe")
                    continue
                
                # Crear persona
                id_persona = conn.execute(
                    text("""
                        INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                           primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                           fecha_nacimiento, genero, direccion, telefono, type)
                        VALUES ('RC', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                :fecha, :genero, :dir, :tel, 'estudiante')
                        RETURNING id_persona
                    """),
                    {
                        "cedula": est['cedula'],
                        "p_nombre": est['primer_nombre'],
                        "s_nombre": est['segundo_nombre'],
                        "p_apellido": est['primer_apellido'],
                        "s_apellido": est['segundo_apellido'],
                        "fecha": est['fecha_nacimiento'],
                        "genero": est['genero'],
                        "dir": est['direccion'],
                        "tel": est['telefono']
                    }
                ).fetchone()[0]
                
                # Crear estudiante
                conn.execute(
                    text("""
                        INSERT INTO estudiante (id_estudiante, codigo_matricula, fecha_ingreso, grado_actual)
                        VALUES (:id_persona, :codigo, CURRENT_TIMESTAMP, :grado)
                    """),
                    {
                        "id_persona": id_persona,
                        "codigo": est['codigo'],
                        "grado": est['grado']
                    }
                )
                
                nombre_completo = f"{est['primer_nombre']} {est['segundo_nombre']} {est['primer_apellido']} {est['segundo_apellido']}"
                print(f"  ✅ Estudiante: {nombre_completo} - {est['grado']} ({est['codigo']})")
            
            # ==================== ASPIRANTES ====================
            print("\n🎯 Creando aspirantes con formularios...")
            aspirantes = [
                {
                    "cedula": "RC-2020003",
                    "primer_nombre": "Camila",
                    "segundo_nombre": "Andrea",
                    "primer_apellido": "Torres",
                    "segundo_apellido": "Gómez",
                    "fecha_nacimiento": "2020-06-10",
                    "genero": "F",
                    "direccion": "Calle 23 #45-67",
                    "telefono": "3145678901",
                    "grado": "Parvulos",
                    "acudiente": {
                        "primer_nombre": "Andrés",
                        "segundo_nombre": "Felipe",
                        "primer_apellido": "Torres",
                        "segundo_apellido": "López",
                        "cedula": "1090909090",
                        "email": "torres.felipe@gmail.com",
                        "telefono": "3145678901",
                        "parentesco": "Padre"
                    }
                },
                {
                    "cedula": "RC-2019002",
                    "primer_nombre": "Nicolás",
                    "segundo_nombre": "Esteban",
                    "primer_apellido": "Vargas",
                    "segundo_apellido": "Mejía",
                    "fecha_nacimiento": "2019-09-14",
                    "genero": "M",
                    "direccion": "Carrera 56 #78-90",
                    "telefono": "3167890123",
                    "grado": "Caminadores",
                    "acudiente": {
                        "primer_nombre": "Carolina",
                        "segundo_nombre": "Isabel",
                        "primer_apellido": "Mejía",
                        "segundo_apellido": "Suárez",
                        "cedula": "1091919191",
                        "email": "carolina.mejia@hotmail.com",
                        "telefono": "3167890123",
                        "parentesco": "Madre"
                    }
                },
                {
                    "cedula": "RC-2018002",
                    "primer_nombre": "Valentina",
                    "segundo_nombre": "Lucía",
                    "primer_apellido": "Castro",
                    "segundo_apellido": "Rincón",
                    "fecha_nacimiento": "2018-12-20",
                    "genero": "F",
                    "direccion": "Calle 90 #12-34",
                    "telefono": "3189012345",
                    "grado": "Prejardin",
                    "acudiente": {
                        "primer_nombre": "Ricardo",
                        "segundo_nombre": "Alberto",
                        "primer_apellido": "Castro",
                        "segundo_apellido": "Pinto",
                        "cedula": "1092929292",
                        "email": "ricardo.castro@yahoo.com",
                        "telefono": "3189012345",
                        "parentesco": "Padre"
                    }
                }
            ]
            
            for asp in aspirantes:
                # Verificar si existe persona aspirante
                existe_persona = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": asp['cedula']}
                ).fetchone()
                
                if existe_persona:
                    print(f"  ⚠️  Aspirante con documento {asp['cedula']} ya existe")
                    continue
                
                # Crear persona acudiente si no existe
                acud_data = asp['acudiente']
                existe_acudiente = conn.execute(
                    text("SELECT id_persona FROM persona WHERE numero_identificacion = :cedula"),
                    {"cedula": acud_data['cedula']}
                ).fetchone()
                
                if existe_acudiente:
                    id_acudiente = existe_acudiente[0]
                else:
                    # Verificar si existe email del acudiente
                    existe_email_acud = conn.execute(
                        text("SELECT id_usuario FROM usuario WHERE correo_electronico = :email"),
                        {"email": acud_data['email']}
                    ).fetchone()
                    
                    if existe_email_acud:
                        # Email ya existe, buscar persona asociada
                        print(f"      ⚠️  Email {acud_data['email']} ya existe, omitiendo acudiente")
                        # Buscar id_persona asociado
                        result = conn.execute(
                            text("SELECT id_acudiente FROM acudiente WHERE id_usuario = :id_usuario"),
                            {"id_usuario": existe_email_acud[0]}
                        ).fetchone()
                        id_acudiente = result[0] if result else None
                        if not id_acudiente:
                            continue
                    else:
                        # Crear persona acudiente
                        id_persona_acud = conn.execute(
                            text("""
                                INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                                   primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                                   genero, direccion, telefono, type)
                                VALUES ('Cédula', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                        'N/A', :dir, :tel, 'acudiente')
                                RETURNING id_persona
                            """),
                            {
                                "cedula": acud_data['cedula'],
                                "p_nombre": acud_data['primer_nombre'],
                                "s_nombre": acud_data['segundo_nombre'],
                                "p_apellido": acud_data['primer_apellido'],
                                "s_apellido": acud_data['segundo_apellido'],
                                "dir": asp['direccion'],
                                "tel": acud_data['telefono']
                            }
                        ).fetchone()[0]
                        
                        # Generar contraseña automática
                        password_acud = f"acud{acud_data['cedula'][-4:]}"
                        
                        # Crear usuario para el acudiente
                        id_usuario_acud = conn.execute(
                            text("""
                                INSERT INTO usuario (correo_electronico, contrasena, id_rol, activo)
                                VALUES (:email, :pwd, :rol, true)
                                RETURNING id_usuario
                            """),
                            {
                                "email": acud_data['email'],
                                "pwd": hash_password(password_acud),
                                "rol": roles['acudiente']
                            }
                        ).fetchone()[0]
                        
                        # Crear acudiente
                        conn.execute(
                            text("""
                                INSERT INTO acudiente (id_acudiente, id_usuario, parentesco)
                                VALUES (:id_persona, :id_usuario, :parentesco)
                            """),
                            {
                                "id_persona": id_persona_acud,
                                "id_usuario": id_usuario_acud,
                                "parentesco": acud_data['parentesco']
                            }
                        )
                        
                        id_acudiente = id_persona_acud
                        
                        # Guardar credenciales
                        nombre_completo_acud = f"{acud_data['primer_nombre']} {acud_data['segundo_nombre']} {acud_data['primer_apellido']} {acud_data['segundo_apellido']}"
                        credenciales.append({
                            'rol': 'Acudiente',
                            'nombre': nombre_completo_acud,
                            'email': acud_data['email'],
                            'password': password_acud,
                            'cedula': acud_data['cedula']
                        })
                        print(f"      ✅ Acudiente creado: {nombre_completo_acud} ({acud_data['email']})")
                
                # Crear persona aspirante
                id_persona_asp = conn.execute(
                    text("""
                        INSERT INTO persona (tipo_identificacion, numero_identificacion,
                                           primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                                           fecha_nacimiento, genero, direccion, telefono, type)
                        VALUES ('RC', :cedula, :p_nombre, :s_nombre, :p_apellido, :s_apellido,
                                :fecha, :genero, :dir, :tel, 'aspirante')
                        RETURNING id_persona
                    """),
                    {
                        "cedula": asp['cedula'],
                        "p_nombre": asp['primer_nombre'],
                        "s_nombre": asp['segundo_nombre'],
                        "p_apellido": asp['primer_apellido'],
                        "s_apellido": asp['segundo_apellido'],
                        "fecha": asp['fecha_nacimiento'],
                        "genero": asp['genero'],
                        "dir": asp['direccion'],
                        "tel": asp['telefono']
                    }
                ).fetchone()[0]
                
                # Crear aspirante
                conn.execute(
                    text("""
                        INSERT INTO aspirante (id_aspirante, grado_solicitado, fecha_solicitud, estado_proceso)
                        VALUES (:id_persona, :grado, CURRENT_TIMESTAMP, 'pendiente')
                    """),
                    {
                        "id_persona": id_persona_asp,
                        "grado": asp['grado']
                    }
                )
                
                # Crear formulario de preinscripción
                datos_aspirante = {
                    "primer_nombre": asp['primer_nombre'],
                    "segundo_nombre": asp['segundo_nombre'],
                    "primer_apellido": asp['primer_apellido'],
                    "segundo_apellido": asp['segundo_apellido'],
                    "tipo_id": "RC",
                    "numero_id": asp['cedula'],
                    "fecha_nacimiento": asp['fecha_nacimiento'],
                    "genero": asp['genero']
                }
                datos_acudiente = {
                    "primer_nombre": acud_data['primer_nombre'],
                    "segundo_nombre": acud_data['segundo_nombre'],
                    "primer_apellido": acud_data['primer_apellido'],
                    "segundo_apellido": acud_data['segundo_apellido'],
                    "cedula": acud_data['cedula'],
                    "email": acud_data['email'],
                    "telefono": acud_data['telefono'],
                    "parentesco": acud_data['parentesco']
                }
                
                conn.execute(
                    text("""
                        INSERT INTO respuesta_form_pre (
                            fecha_solicitud, grado_solicitado,
                            datos_aspirante, datos_acudiente,
                            correo_envio, telefono_contacto
                        )
                        VALUES (CURRENT_TIMESTAMP, :grado, :datos_asp, :datos_acud, :email, :tel)
                    """),
                    {
                        "grado": asp['grado'],
                        "datos_asp": json.dumps(datos_aspirante, ensure_ascii=False),
                        "datos_acud": json.dumps(datos_acudiente, ensure_ascii=False),
                        "email": acud_data['email'],
                        "tel": acud_data['telefono']
                    }
                )
                
                nombre_completo = f"{asp['primer_nombre']} {asp['segundo_nombre']} {asp['primer_apellido']} {asp['segundo_apellido']}"
                print(f"  ✅ Aspirante: {nombre_completo} - {asp['grado']} (Estado: pendiente)")
            
            # Confirmar transacción
            trans.commit()
            print("\n" + "=" * 80)
            print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
            print("=" * 80)
            
            # Guardar credenciales
            guardar_credenciales(credenciales)
            
            # Resumen
            print("\n📊 RESUMEN:")
            print(f"  • Administradores: {len(admins)}")
            print(f"  • Profesores: {len(profesores)}")
            print(f"  • Directivos: {len(directivos)}")
            print(f"  • Acudientes: {len(acudientes)}")
            print(f"  • Estudiantes: {len(estudiantes)}")
            print(f"  • Aspirantes: {len(aspirantes)}")
            print(f"\n  Total usuarios con credenciales: {len(credenciales)}")
            
        except Exception as e:
            trans.rollback()
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    try:
        populate_database()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        sys.exit(1)
