#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Inicialización de Permisos
Crea los permisos en la BD y los asigna a roles
"""

import sys
from pathlib import Path
from sqlalchemy import text

# Configurar salida UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar ruta del proyecto (ir a la raíz desde scripts/)
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data.db import SessionLocal, engine
from app.data.mappers import start_mappers, metadata

print("\n" + "="*70)
print("  INICIALIZACION DE PERMISOS Y CONTROL DE ACCESO")
print("="*70 + "\n")

# Inicializar mappers
start_mappers()

# CREAR TODAS LAS TABLAS (incluyendo permiso y rol_permiso)
print("[*] Creando tablas en la base de datos...")
try:
    metadata.create_all(engine)
    print("[OK] Tablas creadas exitosamente\n")
except Exception as e:
    print(f"[!] Advertencia al crear tablas: {e}\n")

try:
    session = SessionLocal()
    
    # ============================================================
    # 1. CREAR PERMISOS
    # ============================================================
    print("[1] Creando permisos del sistema...\n")
    
    permisos = [
        # Admin
        ("acceder_admin", "Acceso al módulo de administración"),
        ("gestionar_usuarios", "Crear, editar, eliminar usuarios"),
        ("gestionar_roles", "Crear, editar, eliminar roles"),
        ("gestionar_permisos", "Crear, editar, eliminar permisos"),
        
        # Director
        ("acceder_director", "Acceso al módulo de director"),
        ("gestionar_grupos", "Crear, editar, eliminar grupos"),
        ("gestionar_profesores", "Asignar profesores a grupos"),
        ("ver_estudiantes", "Ver lista de estudiantes"),
        
        # Profesor
        ("acceder_profesor", "Acceso al módulo de profesor"),
        ("ver_calificaciones", "Ver calificaciones de estudiantes"),
        ("registrar_calificaciones", "Registrar calificaciones"),
        ("crear_anotaciones", "Crear anotaciones de estudiantes"),
        ("ver_asignaciones", "Ver asignaciones de cursos"),
        
        # Acudiente
        ("acceder_acudiente", "Acceso al módulo de acudiente"),
        ("ver_desempenio", "Ver desempeño del estudiante"),
        ("ver_comunicaciones", "Ver comunicaciones con colegio"),
        
        # Estudiante
        ("acceder_estudiante", "Acceso al módulo de estudiante"),
        ("ver_mis_calificaciones", "Ver sus propias calificaciones"),
        ("ver_mis_anotaciones", "Ver anotaciones sobre él"),
        
        # General
        ("ver_reportes", "Ver reportes del sistema"),
        ("generar_reportes", "Generar reportes"),
        ("ver_citaciones", "Ver citaciones"),
        ("crear_citaciones", "Crear citaciones"),
    ]
    
    permisos_creados = 0
    for nombre, descripcion in permisos:
        # Verificar si ya existe
        existe = session.execute(text("""
            SELECT COUNT(*) FROM permiso WHERE nombre = :nombre
        """), {"nombre": nombre}).scalar()
        
        if not existe:
            session.execute(text("""
                INSERT INTO permiso (nombre, descripcion)
                VALUES (:nombre, :descripcion)
            """), {"nombre": nombre, "descripcion": descripcion})
            
            print(f"   [+] {nombre:<25} - {descripcion}")
            permisos_creados += 1
        else:
            print(f"   [=] {nombre:<25} - (ya existe)")
    
    session.commit()
    print(f"\n   Permisos creados: {permisos_creados}\n")
    
    # ============================================================
    # 2. ASIGNAR PERMISOS A ROLES
    # ============================================================
    print("[2] Asignando permisos a roles...\n")
    
    asignaciones = {
        "Administrador": [
            "acceder_admin", "gestionar_usuarios", "gestionar_roles", 
            "gestionar_permisos", "ver_reportes", "generar_reportes",
            "ver_citaciones", "crear_citaciones"
        ],
        "Director": [
            "acceder_director", "gestionar_grupos", "gestionar_profesores",
            "ver_estudiantes", "ver_reportes", "generar_reportes",
            "ver_citaciones", "crear_citaciones"
        ],
        "Profesor": [
            "acceder_profesor", "ver_calificaciones", "registrar_calificaciones",
            "crear_anotaciones", "ver_asignaciones", "ver_estudiantes",
            "ver_citaciones"
        ],
        "Acudiente": [
            "acceder_acudiente", "ver_desempenio", "ver_comunicaciones"
        ],
        "Estudiante": [
            "acceder_estudiante", "ver_mis_calificaciones", "ver_mis_anotaciones"
        ],
        "Aspirante": [
            "acceder_estudiante"
        ],
    }
    
    asignaciones_creadas = 0
    for nombre_rol, permisos_rol in asignaciones.items():
        # Obtener ID del rol
        rol_result = session.execute(text("""
            SELECT id_rol FROM rol WHERE nombre_rol = :nombre
        """), {"nombre": nombre_rol}).fetchone()
        
        if not rol_result:
            print(f"   [!] Rol '{nombre_rol}' no encontrado, saltando...\n")
            continue
        
        rol_id = rol_result[0]
        print(f"   [*] Rol: {nombre_rol} (ID: {rol_id})")
        
        for nombre_permiso in permisos_rol:
            # Obtener ID del permiso
            permiso_result = session.execute(text("""
                SELECT id_permiso FROM permiso WHERE nombre = :nombre
            """), {"nombre": nombre_permiso}).fetchone()
            
            if not permiso_result:
                print(f"      [!] Permiso '{nombre_permiso}' no encontrado")
                continue
            
            permiso_id = permiso_result[0]
            
            # Verificar si ya está asignado
            ya_existe = session.execute(text("""
                SELECT COUNT(*) FROM rol_permiso 
                WHERE id_rol = :rol_id AND id_permiso = :permiso_id
            """), {"rol_id": rol_id, "permiso_id": permiso_id}).scalar()
            
            if not ya_existe:
                session.execute(text("""
                    INSERT INTO rol_permiso (id_rol, id_permiso)
                    VALUES (:rol_id, :permiso_id)
                """), {"rol_id": rol_id, "permiso_id": permiso_id})
                
                print(f"      [+] {nombre_permiso}")
                asignaciones_creadas += 1
            else:
                print(f"      [=] {nombre_permiso} (ya asignado)")
        
        print()
    
    session.commit()
    print(f"   Asignaciones creadas: {asignaciones_creadas}\n")
    
    # ============================================================
    # 3. VERIFICAR ASIGNACIONES
    # ============================================================
    print("[3] Verificando asignaciones...\n")
    
    for nombre_rol in asignaciones.keys():
        rol_result = session.execute(text("""
            SELECT r.id_rol, COUNT(p.id_permiso) as permisos
            FROM rol r
            LEFT JOIN rol_permiso rp ON r.id_rol = rp.id_rol
            LEFT JOIN permiso p ON rp.id_permiso = p.id_permiso
            WHERE r.nombre_rol = :nombre
            GROUP BY r.id_rol
        """), {"nombre": nombre_rol}).fetchone()
        
        if rol_result:
            rol_id, cantidad_permisos = rol_result
            print(f"   [OK] {nombre_rol:<15} - {cantidad_permisos} permisos asignados")
    
    print("\n" + "="*70)
    print("[OK] INICIALIZACION COMPLETADA EXITOSAMENTE")
    print("="*70 + "\n")
    
    session.close()

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
