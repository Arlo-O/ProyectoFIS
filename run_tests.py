#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba completo para verificar todas las funcionalidades principales
"""

import sys
import os
from pathlib import Path

# Configurar salida UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.data.db import engine, SessionLocal
from sqlalchemy import text

def print_header(title):
    """Imprime un encabezado"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """Imprime un encabezado de sección"""
    print(f"\n{title}")
    print("-" * 60)

def test_imports():
    """TEST 1: Verificar que los imports funcionan"""
    print_section("TEST 1: Validar Imports")
    
    try:
        from app.ui.components.form import create_unified_form
        print("[OK] create_unified_form importado correctamente")
        
        from app.services.servicio_preinscripcion import ServicioPreinscripcion
        print("[OK] ServicioPreinscripcion importado correctamente")
        
        from app.core.preinscripcion.modelo_preinscripcion import IntentoFallo
        print("[OK] Modelos de preinscripción importados correctamente")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error de import: {e}")
        return False

def test_service():
    """TEST 2: Verificar que el servicio funciona"""
    print_section("TEST 2: Validar Servicio de Preinscripción")
    
    try:
        from app.services.servicio_preinscripcion import ServicioPreinscripcion
        
        servicio = ServicioPreinscripcion()
        print("[OK] ServicioPreinscripcion instantiado")
        
        # Registrar error de prueba
        intento = servicio.registrar_error(
            {"nombre": "Nombre invalido"},
            "test_user"
        )
        print(f"[OK] Intento registrado: {intento.numero_error}/3")
        
        # Obtener contador
        contador = servicio.obtener_contador_intentos("test_user")
        print(f"[OK] Contador obtenido: {contador} intentos hoy")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error en servicio: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_form_structure():
    """TEST 3: Verificar que el formulario se puede crear"""
    print_section("TEST 3: Validar Estructura del Formulario")
    
    try:
        import tkinter as tk
        from app.ui.components.form import create_unified_form
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        # Crear formulario
        nav_commands = {'home': lambda: None, 'dashboard': lambda: None}
        form = create_unified_form(root, nav_commands)
        
        print("[OK] Formulario creado exitosamente")
        print(f"[OK] Tipo: {type(form).__name__}")
        print(f"[OK] Widgets en formulario: {len(form.winfo_children())}")
        
        # Limpiar
        root.destroy()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear formulario: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_persistence():
    """TEST 4: Verificar persistencia de datos"""
    print_section("TEST 4: Validar Persistencia (JSON)")
    
    try:
        from app.services.servicio_preinscripcion import ServicioPreinscripcion
        
        servicio = ServicioPreinscripcion()
        usuario = "persistence_test"
        
        # Limpiar intentos previos
        servicio.servicio_intentos.limpiar_intentos_usuario(usuario)
        print("[OK] Base limpiada")
        
        # Registrar 3 intentos
        for i in range(3):
            intento = servicio.registrar_error(
                {f"error_{i}": f"Error tipo {i+1}"},
                usuario
            )
            print(f"[OK] Intento {i+1} registrado")
        
        # Verificar persistencia
        intentos = servicio.servicio_intentos.obtener_intentos_usuario(usuario)
        print(f"[OK] {len(intentos)} intentos recuperados del JSON")
        
        # Verificar contador
        contador = servicio.obtener_contador_intentos(usuario)
        print(f"[OK] Contador verificado: {contador}/3")
        
        # Limpiar
        servicio.servicio_intentos.limpiar_intentos_usuario(usuario)
        
        return True
    except Exception as e:
        print(f"[ERROR] Error de persistencia: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validators():
    """TEST 5: Verificar validadores"""
    print_section("TEST 5: Validar Validadores del Formulario")
    
    try:
        from app.ui.components.form import FormValidators
        
        # Test nombre válido
        valido, error = FormValidators.validar_nombre("Juan Carlos")
        assert valido, "Nombre válido rechazado"
        print("[OK] Validador de nombre: valido")
        
        # Test nombre inválido
        valido, error = FormValidators.validar_nombre("AB")
        assert not valido, "Nombre inválido aceptado"
        print("[OK] Validador de nombre: invalido detectado")
        
        # Test email válido
        valido, error = FormValidators.validar_email("test@example.com")
        assert valido, "Email válido rechazado"
        print("[OK] Validador de email: valido")
        
        # Test email inválido
        valido, error = FormValidators.validar_email("invalid_email")
        assert not valido, "Email inválido aceptado"
        print("[OK] Validador de email: invalido detectado")
        
        # Test cédula válida
        valido, error = FormValidators.validar_cedula("1234567890")
        assert valido, "Cédula válida rechazada"
        print("[OK] Validador de cedula: valido")
        
        # Test teléfono válido
        valido, error = FormValidators.validar_telefono("3001234567")
        assert valido, "Teléfono válido rechazado"
        print("[OK] Validador de telefono: valido")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error en validadores: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scroll_code():
    """TEST 6: Verificar que el código de scroll está presente"""
    print_section("TEST 6: Validar Código de Scroll")
    
    try:
        form_path = Path("app/ui/components/form.py")
        content = form_path.read_text(encoding='utf-8')
        
        # Verificar que el código de scroll está presente
        checks = [
            ("mouse_over_canvas", "Variable de rastreo de mouse"),
            ("_on_mouseenter", "Handler Enter"),
            ("_on_mouseleave", "Handler Leave"),
            ("_on_mousewheel", "Handler MouseWheel"),
            ("_bind_scroll_events", "Binding recursivo"),
            ("return \"break\"", "Prevención de propagación"),
        ]
        
        all_found = True
        for code, description in checks:
            if code in content:
                print(f"[OK] {description}: presente")
            else:
                print(f"[ERROR] {description}: FALTA")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"[ERROR] Error verificando codigo: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print_header("PRUEBAS AUTOMATIZADAS - SISTEMA MVC + SCROLL")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = {
        "Imports": test_imports(),
        "Servicio": test_service(),
        "Estructura del Formulario": test_form_structure(),
        "Persistencia": test_persistence(),
        "Validadores": test_validators(),
        "Código de Scroll": test_scroll_code(),
    }
    
    # Resumen
    print_header("RESUMEN DE RESULTADOS")
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"Total: {passed} pasadas, {failed} fallidas")
    
    if failed == 0:
        print("\n[SUCCESS] TODOS LOS TESTS PASARON CORRECTAMENTE")
        print("\nProximos pasos:")
        print("1. Ejecutar: python test_scroll_form.py")
        print("2. Probar scroll con rueda del mouse")
        print("3. Verificar que funciona en todos los campos")
        return 0
    else:
        print(f"\n[WARNING] {failed} test(s) fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
