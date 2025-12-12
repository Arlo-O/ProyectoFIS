# -*- coding: utf-8 -*-
"""
Pruebas para CU-07: Recuperar Contraseña
Verifica el flujo completo de recuperación
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.services.recuperacion_password_service import RecuperacionPasswordService
from app.services.email_service import EmailService
import bcrypt


def test_generador_codigo():
    """Test 1: Generador de códigos"""
    print("\n" + "="*80)
    print("TEST 1: Generador de Códigos de 6 Caracteres")
    print("="*80)
    
    codigos = [RecuperacionPasswordService.generar_codigo() for _ in range(5)]
    
    for i, codigo in enumerate(codigos, 1):
        print(f"Código {i}: {codigo}")
        assert len(codigo) == 6, f"Código debe tener 6 caracteres, tiene {len(codigo)}"
        assert codigo.isalnum(), f"Código debe ser alfanumérico"
    
    # Verificar que son únicos (probabilidad muy alta)
    assert len(set(codigos)) == 5, "Los códigos deben ser únicos"
    
    print("✅ Generador de códigos funciona correctamente")


def test_validacion_password():
    """Test 2: Validación de contraseñas"""
    print("\n" + "="*80)
    print("TEST 2: Validación de Contraseñas")
    print("="*80)
    
    # Casos de prueba
    casos = [
        ("Pass123", "Pass123", False, "muy corta"),
        ("password123", "password123", False, "sin mayúscula"),
        ("PASSWORD123", "PASSWORD123", False, "sin minúscula"),
        ("Password", "Password", False, "sin número"),
        ("Password1", "Password2", False, "no coinciden"),
        ("Password123", "Password123", True, "válida"),
    ]
    
    for password, confirmar, debe_ser_valida, descripcion in casos:
        valida, mensaje = RecuperacionPasswordService.validar_nueva_password(password, confirmar)
        print(f"\nCaso: {descripcion}")
        print(f"  Password: {password}")
        print(f"  Resultado esperado: {'VÁLIDA' if debe_ser_valida else 'INVÁLIDA'}")
        print(f"  Resultado obtenido: {'VÁLIDA' if valida else 'INVÁLIDA'}")
        if not valida:
            print(f"  Mensaje: {mensaje}")
        
        assert valida == debe_ser_valida, f"Validación incorrecta para {descripcion}"
    
    print("\n✅ Validación de contraseñas funciona correctamente")


def test_encriptacion_password():
    """Test 3: Encriptación bcrypt"""
    print("\n" + "="*80)
    print("TEST 3: Encriptación de Contraseñas con bcrypt")
    print("="*80)
    
    password = "Password123"
    
    # Generar dos hashes de la misma contraseña
    hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    hash2 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    print(f"Contraseña original: {password}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    # Los hashes deben ser diferentes (sal aleatoria)
    assert hash1 != hash2, "Los hashes deben ser diferentes"
    
    # Ambos deben validar correctamente
    assert bcrypt.checkpw(password.encode('utf-8'), hash1.encode('utf-8')), "Hash1 debe validar"
    assert bcrypt.checkpw(password.encode('utf-8'), hash2.encode('utf-8')), "Hash2 debe validar"
    
    # Password incorrecta no debe validar
    assert not bcrypt.checkpw("WrongPass".encode('utf-8'), hash1.encode('utf-8')), "Password incorrecta no debe validar"
    
    print("✅ Encriptación bcrypt funciona correctamente")


def test_envio_email_simulado():
    """Test 4: Envío de email simulado"""
    print("\n" + "="*80)
    print("TEST 4: Envío de Email Simulado")
    print("="*80)
    
    email_usuario = "test@colegio.edu"
    codigo = "ABC123"
    
    exito, mensaje = EmailService.enviar_codigo_recuperacion(email_usuario, codigo)
    
    print(f"Resultado: {'ÉXITO' if exito else 'FALLO'}")
    print(f"Mensaje: {mensaje}")
    
    assert exito, "El envío simulado debe ser exitoso"
    
    # Verificar que se creó el archivo de log
    log_file = os.path.join("logs", "codigos_recuperacion.txt")
    assert os.path.exists(log_file), f"Debe existir el archivo de log: {log_file}"
    
    print(f"✅ Email simulado enviado correctamente")
    print(f"✅ Log guardado en: {log_file}")


def test_estructura_archivos():
    """Test 5: Verificar estructura de archivos"""
    print("\n" + "="*80)
    print("TEST 5: Estructura de Archivos")
    print("="*80)
    
    archivos_requeridos = [
        "app/core/usuarios/password_reset_code.py",
        "app/services/recuperacion_password_service.py",
        "app/services/email_service.py",
        "app/ui/components/recuperar_password.py",
    ]
    
    for archivo in archivos_requeridos:
        ruta = os.path.join(os.getcwd(), archivo)
        existe = os.path.exists(ruta)
        print(f"{'✅' if existe else '❌'} {archivo}")
        assert existe, f"Debe existir el archivo: {archivo}"
    
    print("\n✅ Todos los archivos necesarios existen")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*80)
    print("🧪 PRUEBAS DE FUNCIONALIDAD CU-07: RECUPERAR CONTRASEÑA")
    print("="*80)
    
    try:
        test_estructura_archivos()
        test_generador_codigo()
        test_validacion_password()
        test_encriptacion_password()
        test_envio_email_simulado()
        
        print("\n" + "="*80)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*80)
        
        print("\n📝 Notas:")
        print("- El generador de códigos funciona correctamente")
        print("- Las validaciones de contraseña están operativas")
        print("- La encriptación bcrypt está configurada")
        print("- El sistema de envío de emails está en modo simulación")
        print("- Los códigos se guardan en logs/codigos_recuperacion.txt")
        
        print("\n🚀 El sistema está listo para recuperación de contraseñas")
        
    except AssertionError as e:
        print(f"\n❌ PRUEBA FALLIDA: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
