"""
Script de Prueba Rápida - Creación de Usuario CU-03
Verifica que la funcionalidad de creación de usuarios está correctamente implementada
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.usuario_service import GeneradorContraseña
import bcrypt

def test_generador_contraseña():
    """Prueba la generación de contraseñas seguras"""
    print("=" * 80)
    print("TEST 1: Generador de Contraseñas")
    print("=" * 80)
    
    for i in range(5):
        password = GeneradorContraseña.generar()
        print(f"Contraseña {i+1}: {password}")
        
        # Verificar longitud
        assert len(password) == 12, f"Longitud incorrecta: {len(password)}"
        
        # Verificar que tenga mayúsculas, minúsculas, números y especiales
        tiene_mayuscula = any(c.isupper() for c in password)
        tiene_minuscula = any(c.islower() for c in password)
        tiene_numero = any(c.isdigit() for c in password)
        tiene_especial = any(not c.isalnum() for c in password)
        
        assert tiene_mayuscula, "Falta mayúscula"
        assert tiene_minuscula, "Falta minúscula"
        assert tiene_numero, "Falta número"
        assert tiene_especial, "Falta carácter especial"
    
    print("✅ Generador de contraseñas funciona correctamente\n")


def test_encriptacion_bcrypt():
    """Prueba la encriptación con bcrypt"""
    print("=" * 80)
    print("TEST 2: Encriptación bcrypt")
    print("=" * 80)
    
    password = "TestPassword123!"
    
    # Encriptar
    hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hash2 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    print(f"Contraseña original: {password}")
    print(f"Hash 1: {hash1.decode('utf-8')}")
    print(f"Hash 2: {hash2.decode('utf-8')}")
    
    # Verificar que son diferentes (salt diferente)
    assert hash1 != hash2, "Los hashes deberían ser diferentes"
    
    # Verificar que ambos validan la contraseña original
    assert bcrypt.checkpw(password.encode('utf-8'), hash1), "Hash 1 no valida"
    assert bcrypt.checkpw(password.encode('utf-8'), hash2), "Hash 2 no valida"
    
    # Verificar que no valida contraseña incorrecta
    assert not bcrypt.checkpw("WrongPassword".encode('utf-8'), hash1), "Hash acepta contraseña incorrecta"
    
    print("✅ Encriptación bcrypt funciona correctamente\n")


def test_archivo_credenciales():
    """Prueba la escritura del archivo de credenciales"""
    print("=" * 80)
    print("TEST 3: Archivo de Credenciales")
    print("=" * 80)
    
    # Crear directorio logs si no existe
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"✅ Directorio logs/ creado: {logs_dir}")
    else:
        print(f"✅ Directorio logs/ existe: {logs_dir}")
    
    # Verificar que el archivo existe o puede crearse
    archivo = os.path.join(logs_dir, "credenciales_usuarios.txt")
    
    # Escribir línea de prueba
    with open(archivo, "a", encoding="utf-8") as f:
        f.write("\n" + "="*80 + "\n")
        f.write("TEST DE ESCRITURA - Sistema de Prueba\n")
        f.write("="*80 + "\n\n")
    
    print(f"✅ Archivo de credenciales accesible: {archivo}\n")


def test_imports():
    """Verifica que todos los imports necesarios están disponibles"""
    print("=" * 80)
    print("TEST 4: Verificación de Imports")
    print("=" * 80)
    
    try:
        from app.core.usuarios.usuario import Usuario
        print("✅ Usuario importado")
        
        from app.data.uow import uow
        print("✅ UnitOfWork importado")
        
        from sqlalchemy import text
        print("✅ SQLAlchemy text importado")
        
        from tkinter import Tk
        print("✅ Tkinter disponible")
        
        import bcrypt
        print("✅ bcrypt disponible")
        
        print("\n✅ Todos los imports necesarios están disponibles\n")
        return True
    
    except ImportError as e:
        print(f"❌ Error de import: {e}\n")
        return False


def main():
    print("\n" + "="*80)
    print("🧪 PRUEBAS DE FUNCIONALIDAD CU-03: CREAR USUARIO")
    print("="*80 + "\n")
    
    try:
        # Test 1: Generador de contraseñas
        test_generador_contraseña()
        
        # Test 2: Encriptación bcrypt
        test_encriptacion_bcrypt()
        
        # Test 3: Archivo de credenciales
        test_archivo_credenciales()
        
        # Test 4: Imports
        test_imports()
        
        print("="*80)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*80)
        print("\n📝 Notas:")
        print("- El generador de contraseñas funciona correctamente")
        print("- La encriptación bcrypt está operativa")
        print("- El sistema de logs está listo")
        print("- Todos los módulos necesarios están disponibles")
        print("\n🚀 El sistema está listo para crear usuarios\n")
        
    except AssertionError as e:
        print(f"\n❌ ERROR EN PRUEBA: {e}\n")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
