#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔄 SCRIPT COMPLETO DE REINICIO DE BASE DE DATOS
================================================
Este script ejecuta el proceso completo de reinicio:
1. Limpia y recrea la estructura de la BD (via SQL)
2. Crea usuarios de prueba con passwords hasheados
3. Carga permisos y los asigna a roles

IMPORTANTE: Ejecutar este script después de correr clean_database.sql en pgAdmin
"""

import sys
from pathlib import Path
import subprocess
import time

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

print("\n" + "="*80)
print("  🔄 REINICIO COMPLETO DE BASE DE DATOS")
print("="*80 + "\n")

# ============================================================
# PASO 1: INSTRUCCIONES PARA SQL
# ============================================================
print("📋 PASO 1: Ejecutar Script SQL")
print("-" * 80)
print("⚠️  ANTES DE CONTINUAR, debes ejecutar en pgAdmin:")
print("    scripts/clean_database.sql")
print("")
print("Este script:")
print("  - Elimina todos los datos")
print("  - Recrea todas las tablas")
print("  - Inserta los 5 roles base")
print("-" * 80)

respuesta = input("\n¿Ya ejecutaste clean_database.sql en pgAdmin? (s/n): ")
if respuesta.lower() != 's':
    print("\n❌ Proceso cancelado. Por favor ejecuta el script SQL primero.")
    sys.exit(0)

# ============================================================
# PASO 2: CREAR USUARIOS DE PRUEBA
# ============================================================
print("\n" + "="*80)
print("📋 PASO 2: Crear Usuarios de Prueba")
print("-" * 80)

try:
    print("🔧 Ejecutando scripts/create_test_users.py...\n")
    
    # Ejecutar script de creación de usuarios
    resultado = subprocess.run(
        [sys.executable, "scripts/create_test_users.py"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    
    # Mostrar output
    if resultado.stdout:
        print(resultado.stdout)
    
    if resultado.returncode != 0:
        print("❌ ERROR al crear usuarios:")
        if resultado.stderr:
            print(resultado.stderr)
        sys.exit(1)
    
    print("✅ Usuarios creados exitosamente\n")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# Pausa breve para asegurar que los commits se completen
time.sleep(1)

# ============================================================
# PASO 3: CARGAR PERMISOS
# ============================================================
print("="*80)
print("📋 PASO 3: Cargar Permisos y Asignar a Roles")
print("-" * 80)

try:
    print("🔧 Ejecutando seed_permisos.py...\n")
    
    # Ejecutar script de permisos
    resultado = subprocess.run(
        [sys.executable, "scripts/seed_permisos.py"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    
    # Mostrar output
    if resultado.stdout:
        print(resultado.stdout)
    
    if resultado.returncode != 0:
        print("❌ ERROR al cargar permisos:")
        if resultado.stderr:
            print(resultado.stderr)
        sys.exit(1)
    
    print("✅ Permisos cargados exitosamente\n")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "="*80)
print("  ✅ REINICIO COMPLETADO EXITOSAMENTE")
print("="*80 + "\n")

print("📊 Usuarios de Prueba Creados:")
print("   👤 admin      | correo: admin@fis.edu.co        | contraseña: admin123")
print("   👤 director   | correo: director@fis.edu.co     | contraseña: director123")
print("   👤 profesor   | correo: profesor@fis.edu.co     | contraseña: profesor123")
print("   👤 padre      | correo: padre@fis.edu.co        | contraseña: padre123")

print("\n🔐 Permisos asignados por rol:")
print("   - Administrador: Todos los permisos (incluye acceder_admin)")
print("   - Director: Gestión de grupos, profesores, estudiantes, reportes")
print("   - Profesor: Calificaciones, anotaciones, asignaciones")
print("   - Acudiente: Ver desempeño y comunicaciones")

print("\n🚀 La aplicación está lista para usar:")
print("   python run_app.py")

print("\n" + "="*80 + "\n")
