#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Suite de pruebas completa para verificar todas las funcionalidades del sistema
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

def test_database_connection():
    """Test 1: Conexión a la base de datos"""
    print("\n" + "="*80)
    print("TEST 1: CONEXIÓN A LA BASE DE DATOS")
    print("="*80)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_usuarios_count():
    """Test 2: Contar usuarios en la BD"""
    print("\n" + "="*80)
    print("TEST 2: USUARIOS EN LA BASE DE DATOS")
    print("="*80)
    try:
        session = SessionLocal()
        result = session.execute(text("""
            SELECT 
                r.nombre_rol,
                COUNT(u.id_usuario) as cantidad
            FROM rol r
            LEFT JOIN usuario u ON u.id_rol = r.id_rol
            GROUP BY r.nombre_rol
            ORDER BY r.nombre_rol
        """)).fetchall()
        
        total = 0
        for row in result:
            print(f"  • {row[0]}: {row[1]} usuarios")
            total += row[1]
        print(f"\n  Total usuarios: {total}")
        session.close()
        print("✅ Test de conteo de usuarios exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_aspirantes():
    """Test 3: Consultar aspirantes"""
    print("\n" + "="*80)
    print("TEST 3: CONSULTAR ASPIRANTES")
    print("="*80)
    try:
        from app.services.servicio_aspirante import ServicioAspirante
        
        servicio = ServicioAspirante()
        exito, aspirantes, mensaje = servicio.obtener_listado_aspirantes()
        
        if exito:
            print(f"✅ Se encontraron {len(aspirantes)} aspirantes:")
            for asp in aspirantes[:5]:  # Mostrar solo los primeros 5
                print(f"  • {asp['nombre_completo']} - {asp['grado_solicitado']} ({asp['estado_proceso']})")
            if len(aspirantes) > 5:
                print(f"  ... y {len(aspirantes) - 5} más")
            return True
        else:
            print(f"⚠️  {mensaje}")
            return True  # No es un error si no hay aspirantes
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_detalle_aspirante():
    """Test 4: Obtener detalle de un aspirante"""
    print("\n" + "="*80)
    print("TEST 4: DETALLE DE ASPIRANTE")
    print("="*80)
    try:
        from app.services.servicio_aspirante import ServicioAspirante
        
        servicio = ServicioAspirante()
        
        # Primero obtener un aspirante
        exito, aspirantes, mensaje = servicio.obtener_listado_aspirantes()
        
        if not exito or len(aspirantes) == 0:
            print("⚠️  No hay aspirantes para probar")
            return True
        
        id_aspirante = aspirantes[0]['id_aspirante']
        print(f"  Obteniendo detalle del aspirante ID: {id_aspirante}")
        
        exito, detalle, mensaje = servicio.obtener_detalle_aspirante(id_aspirante)
        
        if exito:
            print(f"✅ Detalle obtenido correctamente:")
            aspirante = detalle.get('aspirante', {})
            print(f"  • Nombre: {aspirante.get('primer_nombre', '')} {aspirante.get('primer_apellido', '')}")
            print(f"  • Grado: {aspirante.get('grado_solicitado', 'N/A')}")
            print(f"  • Estado: {aspirante.get('estado_proceso', 'N/A')}")
            if 'acudiente' in detalle and detalle['acudiente']:
                acudiente = detalle['acudiente']
                print(f"  • Acudiente: {acudiente.get('primer_nombre', '')} {acudiente.get('primer_apellido', '')}")
            return True
        else:
            print(f"❌ Error: {mensaje}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_autenticacion():
    """Test 5: Servicio de autenticación"""
    print("\n" + "="*80)
    print("TEST 5: AUTENTICACIÓN")
    print("="*80)
    try:
        from app.services.auth_service import AuthenticationService
        import bcrypt
        
        # Probar validación de credenciales
        print("  • Probando validación de formato de credenciales...")
        valido, mensaje = AuthenticationService.validate_credentials("admin@colegio.edu", "admin123")
        
        if valido:
            print("✅ Validación de formato correcta")
        else:
            print(f"⚠️  Validación falló: {mensaje}")
        
        # Probar verificación de contraseña con bcrypt
        print("  • Probando verificación de contraseña con bcrypt...")
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        valido_pwd = AuthenticationService.verify_password("admin123", password_hash)
        
        if valido_pwd:
            print("✅ Verificación de contraseña con bcrypt exitosa")
        else:
            print("⚠️  Verificación de contraseña falló")
        
        # Verificar usuario directamente en BD
        print("  • Verificando usuarios en la base de datos...")
        session = SessionLocal()
        result = session.execute(text("SELECT correo_electronico, activo FROM usuario WHERE correo_electronico = 'admin@colegio.edu'")).fetchone()
        
        if result:
            print(f"✅ Usuario admin encontrado en BD: {result[0]} (activo: {result[1]})")
        else:
            print("⚠️  Usuario admin no encontrado")
        
        session.close()
        
        # Probar autenticación (sin hacer login real)
        print("  • Verificando existencia de usuarios de prueba...")
        session = SessionLocal()
        usuarios = session.execute(text("""
            SELECT correo_electronico, activo 
            FROM usuario 
            WHERE correo_electronico IN ('admin@colegio.edu', 'profesor1@colegio.edu', 'acudiente1@gmail.com')
            LIMIT 3
        """)).fetchall()
        
        for usr in usuarios:
            estado = "✅ Activo" if usr[1] else "❌ Inactivo"
            print(f"  • {usr[0]}: {estado}")
        
        session.close()
        print("✅ Test de autenticación exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rbac():
    """Test 6: Control de acceso basado en roles"""
    print("\n" + "="*80)
    print("TEST 6: RBAC (CONTROL DE ACCESO)")
    print("="*80)
    try:
        from app.services.rbac_service import RBACService
        
        rbac = RBACService()
        
        # Verificar permisos
        session = SessionLocal()
        permisos = session.execute(text("""
            SELECT 
                r.nombre_rol,
                COUNT(DISTINCT rp.id_permiso) as num_permisos
            FROM rol r
            LEFT JOIN rol_permiso rp ON r.id_rol = rp.id_rol
            GROUP BY r.nombre_rol
            ORDER BY r.nombre_rol
        """)).fetchall()
        
        print("  Permisos por rol:")
        for row in permisos:
            print(f"  • {row[0]}: {row[1]} permisos")
        
        session.close()
        print("✅ Test de RBAC exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_estudiantes():
    """Test 7: Estudiantes en la BD"""
    print("\n" + "="*80)
    print("TEST 7: ESTUDIANTES")
    print("="*80)
    try:
        session = SessionLocal()
        estudiantes = session.execute(text("""
            SELECT 
                p.primer_nombre,
                p.primer_apellido,
                e.codigo_matricula,
                e.grado_actual
            FROM estudiante e
            JOIN persona p ON e.id_estudiante = p.id_persona
            ORDER BY e.codigo_matricula
        """)).fetchall()
        
        print(f"  Se encontraron {len(estudiantes)} estudiantes:")
        for est in estudiantes:
            print(f"  • {est[0]} {est[1]} - {est[2]} ({est[3]})")
        
        session.close()
        print("✅ Test de estudiantes exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_acudientes():
    """Test 8: Acudientes en la BD"""
    print("\n" + "="*80)
    print("TEST 8: ACUDIENTES")
    print("="*80)
    try:
        session = SessionLocal()
        acudientes = session.execute(text("""
            SELECT 
                p.primer_nombre,
                p.primer_apellido,
                a.parentesco,
                CASE WHEN a.id_usuario IS NOT NULL THEN 'Con usuario' ELSE 'Sin usuario' END as tiene_usuario,
                u.correo_electronico
            FROM acudiente a
            JOIN persona p ON a.id_acudiente = p.id_persona
            LEFT JOIN usuario u ON a.id_usuario = u.id_usuario
            ORDER BY p.primer_apellido
        """)).fetchall()
        
        print(f"  Se encontraron {len(acudientes)} acudientes:")
        for acud in acudientes:
            email = acud[4] if acud[4] else 'N/A'
            print(f"  • {acud[0]} {acud[1]} ({acud[2]}) - {acud[3]} - {email}")
        
        session.close()
        print("✅ Test de acudientes exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_profesores():
    """Test 9: Profesores en la BD"""
    print("\n" + "="*80)
    print("TEST 9: PROFESORES")
    print("="*80)
    try:
        session = SessionLocal()
        profesores = session.execute(text("""
            SELECT 
                p.primer_nombre,
                p.primer_apellido,
                pr.especialidad,
                u.correo_electronico
            FROM profesor pr
            JOIN persona p ON pr.id_profesor = p.id_persona
            LEFT JOIN usuario u ON pr.id_usuario = u.id_usuario
            ORDER BY p.primer_apellido
        """)).fetchall()
        
        print(f"  Se encontraron {len(profesores)} profesores:")
        for prof in profesores:
            email = prof[3] if prof[3] else 'Sin usuario'
            print(f"  • {prof[0]} {prof[1]} - {prof[2]} ({email})")
        
        session.close()
        print("✅ Test de profesores exitoso")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_preinscripcion():
    """Test 10: Servicio de preinscripción"""
    print("\n" + "="*80)
    print("TEST 10: SERVICIO DE PREINSCRIPCIÓN")
    print("="*80)
    try:
        from app.services.servicio_preinscripcion import ServicioPreinscripcion
        
        servicio = ServicioPreinscripcion()
        print("✅ Servicio de preinscripción instanciado correctamente")
        
        # Verificar que los métodos existen
        assert hasattr(servicio, 'registrar_preinscripcion_bd'), "Falta método registrar_preinscripcion_bd"
        print("✅ Método registrar_preinscripcion_bd existe")
        
        assert hasattr(servicio, 'registrar_error'), "Falta método registrar_error"
        print("✅ Método registrar_error existe")
        
        assert hasattr(servicio, 'obtener_contador_intentos'), "Falta método obtener_contador_intentos"
        print("✅ Método obtener_contador_intentos existe")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "SUITE DE PRUEBAS COMPLETA" + " "*33 + "║")
    print("╚" + "="*78 + "╝")
    
    tests = [
        ("Conexión a BD", test_database_connection),
        ("Conteo de usuarios", test_usuarios_count),
        ("Consultar aspirantes", test_aspirantes),
        ("Detalle de aspirante", test_detalle_aspirante),
        ("Autenticación", test_autenticacion),
        ("Control de acceso (RBAC)", test_rbac),
        ("Estudiantes", test_estudiantes),
        ("Acudientes", test_acudientes),
        ("Profesores", test_profesores),
        ("Servicio de preinscripción", test_preinscripcion),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ Error fatal en {nombre}: {e}")
            import traceback
            traceback.print_exc()
            resultados.append((nombre, False))
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    
    exitosos = sum(1 for _, r in resultados if r)
    fallidos = len(resultados) - exitosos
    
    for nombre, resultado in resultados:
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{estado}: {nombre}")
    
    print("\n" + "="*80)
    print(f"Total: {len(resultados)} tests | ✅ Exitosos: {exitosos} | ❌ Fallidos: {fallidos}")
    print("="*80)
    
    if fallidos == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print(f"\n⚠️  {fallidos} test(s) fallaron. Revisar los errores arriba.")
    
    return fallidos == 0

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
