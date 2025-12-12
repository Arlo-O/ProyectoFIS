"""
database.py - Inicialización de la Base de Datos

Script para:
1. Crear todas las tablas necesarias
2. Insertar datos iniciales (roles, configuraciones)
3. Verificar la conexión a la BD
"""

import os
import sys
from pathlib import Path

# Agregar ruta raíz
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.data.db import engine, mapper_registry
from app.data.mappers import start_mappers
from app.config.settings import DATABASE_URL, IS_DEVELOPMENT


def create_tables():
    """
    Crea todas las tablas en la base de datos si no existen.
    
    Ejecuta el schema SQL generado por SQLAlchemy desde los mappers.
    """
    print("=" * 70)
    print("INICIANDO CREACIÓN DE TABLAS...")
    print("=" * 70)
    
    try:
        # Inicializar mappers
        start_mappers()
        
        # Crear todas las tablas
        mapper_registry.metadata.create_all(engine)
        
        print("[✓] Tablas creadas exitosamente")
        print(f"[✓] Conectado a: {DATABASE_URL}")
        return True
        
    except Exception as e:
        print(f"[✗] Error al crear tablas: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_connection():
    """
    Verifica que la conexión a la BD funciona correctamente.
    """
    print("\n" + "=" * 70)
    print("VERIFICANDO CONEXIÓN A BD...")
    print("=" * 70)
    
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("[✓] Conexión exitosa a la base de datos")
            return True
    except Exception as e:
        print(f"[✗] Error de conexión: {e}")
        return False


def initialize_database():
    """
    Función principal para inicializar la BD completamente.
    
    Ejecutar una sola vez:
        python -c "from app.config.database import initialize_database; initialize_database()"
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "INICIALIZADOR DE BASE DE DATOS" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Paso 1: Verificar conexión
    if not verify_connection():
        print("\n[!] No se puede continuar sin conexión a BD.")
        return False
    
    # Paso 2: Crear tablas
    if not create_tables():
        print("\n[!] Error al crear tablas.")
        return False
    
    print("\n" + "=" * 70)
    print("[✓] BASE DE DATOS INICIALIZADA EXITOSAMENTE")
    print("=" * 70)
    print("\nPróximos pasos:")
    print("1. Insertar datos de prueba: python app/config/initial_data.py")
    print("2. Iniciar la aplicación: python run_app.py")
    print()
    
    return True


if __name__ == "__main__":
    initialize_database()
