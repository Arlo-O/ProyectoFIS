"""
Test del CU-19: Crear Hoja de Vida del Estudiante
Verifica el funcionamiento del servicio y validaciones
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.services.servicio_hoja_vida import ServicioHojaVida
from app.services.servicio_aspirante import ServicioAspirante


def test_cu19_crear_hoja_vida():
    """
    Prueba el flujo completo del CU-19
    """
    print("=" * 70)
    print("TEST CU-19: CREAR HOJA DE VIDA DEL ESTUDIANTE")
    print("=" * 70)
    print()
    
    # Inicializar servicios
    servicio_aspirante = ServicioAspirante()
    servicio_hoja_vida = ServicioHojaVida()
    
    # PASO 1: Buscar un aspirante admitido
    print("PASO 1: Buscando aspirantes admitidos...")
    exito, aspirantes, mensaje = servicio_aspirante.obtener_listado_aspirantes()
    
    if not exito or not aspirantes:
        print(f"✗ No hay aspirantes disponibles: {mensaje}")
        return
    
    # Filtrar solo admitidos
    aspirantes_admitidos = [a for a in aspirantes if a['estado_proceso'] == 'admitido']
    
    if not aspirantes_admitidos:
        print("✗ No hay aspirantes admitidos para crear hoja de vida")
        print("  Primero debe admitir un aspirante usando el CU-18")
        return
    
    print(f"✓ Se encontraron {len(aspirantes_admitidos)} aspirantes admitidos")
    print()
    
    # Mostrar aspirantes admitidos
    print("Aspirantes admitidos disponibles:")
    print("-" * 70)
    for i, asp in enumerate(aspirantes_admitidos[:5], 1):
        print(f"{i}. ID: {asp['id_aspirante']:3} | {asp['nombre_completo']:30}")
    print()
    
    # Seleccionar el primero
    aspirante = aspirantes_admitidos[0]
    id_aspirante = aspirante['id_aspirante']
    nombre = aspirante['nombre_completo']
    
    print(f"ASPIRANTE SELECCIONADO:")
    print(f"  ID: {id_aspirante}")
    print(f"  Nombre: {nombre}")
    print()
    
    # PASO 2: Cargar datos del estudiante admitido
    print("PASO 2: Cargando datos del estudiante admitido...")
    exito, datos, mensaje = servicio_hoja_vida.cargar_datos_estudiante_admitido(id_aspirante)
    
    if not exito:
        print(f"✗ Error: {mensaje}")
        return
    
    print("✓ Datos cargados exitosamente:")
    print(f"  - Nombre: {datos['nombre_completo']}")
    print(f"  - Identificación: {datos['tipo_identificacion']} {datos['numero_identificacion']}")
    print(f"  - Grado: {datos['grado_solicitado']}")
    print()
    
    # PASO 3: Cargar formato base
    print("PASO 3: Cargando formato base de hoja de vida...")
    formato = servicio_hoja_vida.obtener_formato_base_hoja_vida()
    
    print("✓ Formato cargado:")
    print(f"  - Campos automáticos: {len(formato['campos_automaticos']['campos'])}")
    print(f"  - Campos obligatorios a diligenciar: {len(formato['campos_faltantes']['campos_obligatorios'])}")
    print(f"  - Campos opcionales: {len(formato['campos_faltantes']['campos_opcionales'])}")
    print()
    
    # PASO 7: Inicializar contador
    print("PASO 7: Inicializando contador de intentos...")
    contador = servicio_hoja_vida.inicializar_contador_intentos(id_aspirante)
    print(f"✓ Contador inicializado: {contador}/{servicio_hoja_vida.LIMITE_INTENTOS}")
    print()
    
    # PASO 6-8: Simular diligenciamiento
    print("PASO 6-8: Simulando diligenciamiento de datos...")
    print()
    
    # Menú de pruebas
    print("=" * 70)
    print("OPCIONES DE PRUEBA:")
    print("=" * 70)
    print("1. Validar datos CORRECTOS (debe pasar)")
    print("2. Validar datos INCORRECTOS - campos vacíos (debe fallar)")
    print("3. Validar datos INCORRECTOS - código corto (debe fallar)")
    print("4. Simular 3 intentos fallidos (límite alcanzado)")
    print("5. Crear hoja de vida con datos completos")
    print("6. Salir")
    print()
    
    opcion = input("Seleccione una opción (1-6): ").strip()
    print()
    
    if opcion == "1":
        # PRUEBA: Validación correcta
        print("PRUEBA 1: VALIDACIÓN DE DATOS CORRECTOS")
        print("-" * 70)
        
        datos_correctos = {
            "codigo_matricula": "EST2025001",
            "estado_salud": "Saludable, sin condiciones médicas conocidas",
            "alergias": ["Polen", "Penicilina"],
            "tratamientos": ["Inhalador para asma"],
            "necesidades_educativas": []
        }
        
        print("Datos a validar:")
        print(f"  - Código: {datos_correctos['codigo_matricula']}")
        print(f"  - Estado salud: {datos_correctos['estado_salud']}")
        print(f"  - Alergias: {', '.join(datos_correctos['alergias'])}")
        print()
        
        formato_correcto, campos_error, errores = servicio_hoja_vida.validar_formato_datos(datos_correctos)
        
        if formato_correcto:
            print("✓ VALIDACIÓN EXITOSA")
            print("  Todos los campos son correctos")
        else:
            print(f"✗ VALIDACIÓN FALLIDA")
            print(f"  Campos con error: {campos_error}")
            for campo, error in errores.items():
                print(f"    • {campo}: {error}")
    
    elif opcion == "2":
        # PRUEBA: Validación con campos vacíos
        print("PRUEBA 2: VALIDACIÓN CON CAMPOS VACÍOS")
        print("-" * 70)
        
        datos_vacios = {
            "codigo_matricula": "",
            "estado_salud": "",
            "alergias": [],
            "tratamientos": [],
            "necesidades_educativas": []
        }
        
        print("Intentando validar con campos vacíos...")
        print()
        
        formato_correcto, campos_error, errores = servicio_hoja_vida.validar_formato_datos(datos_vacios)
        
        if not formato_correcto:
            print("✓ VALIDACIÓN CORRECTA (detectó errores)")
            print(f"  Campos con error: {len(campos_error)}")
            for campo, error in errores.items():
                print(f"    • {error}")
        else:
            print("✗ ERROR: El sistema NO detectó los campos vacíos")
    
    elif opcion == "3":
        # PRUEBA: Validación con código corto
        print("PRUEBA 3: VALIDACIÓN CON CÓDIGO INVÁLIDO")
        print("-" * 70)
        
        datos_invalidos = {
            "codigo_matricula": "ABC",  # Muy corto
            "estado_salud": "OK",  # Muy corto
            "alergias": [],
            "tratamientos": [],
            "necesidades_educativas": []
        }
        
        print("Datos a validar:")
        print(f"  - Código: '{datos_invalidos['codigo_matricula']}' (3 caracteres - inválido)")
        print(f"  - Estado salud: '{datos_invalidos['estado_salud']}' (2 caracteres - inválido)")
        print()
        
        formato_correcto, campos_error, errores = servicio_hoja_vida.validar_formato_datos(datos_invalidos)
        
        if not formato_correcto:
            print("✓ VALIDACIÓN CORRECTA (detectó errores de formato)")
            print(f"  Campos con error: {len(campos_error)}")
            for campo, error in errores.items():
                print(f"    • {error}")
        else:
            print("✗ ERROR: El sistema NO detectó los errores de formato")
    
    elif opcion == "4":
        # PRUEBA: Límite de intentos
        print("PRUEBA 4: SIMULAR LÍMITE DE 3 INTENTOS")
        print("-" * 70)
        
        datos_invalidos = {
            "codigo_matricula": "",
            "estado_salud": "",
            "alergias": [],
            "tratamientos": [],
            "necesidades_educativas": []
        }
        
        for intento in range(1, 4):
            print(f"\nINTENTO {intento}:")
            
            # Incrementar contador
            contador_actual = servicio_hoja_vida.incrementar_contador(id_aspirante)
            print(f"  Contador: {contador_actual}/{servicio_hoja_vida.LIMITE_INTENTOS}")
            
            # Validar
            formato_correcto, campos_error, errores = servicio_hoja_vida.validar_formato_datos(datos_invalidos)
            
            if not formato_correcto:
                print(f"  ✗ Validación fallida: {len(campos_error)} errores")
                
                if contador_actual < servicio_hoja_vida.LIMITE_INTENTOS:
                    print("  → El formulario permanece abierto para correcciones")
                else:
                    print("  → LÍMITE ALCANZADO: El proceso se cancela")
                    print("  → Los datos NO se guardan")
        
        print()
        print("✓ Simulación completada")
        print(f"  Contador final: {servicio_hoja_vida.obtener_contador(id_aspirante)}")
    
    elif opcion == "5":
        # PRUEBA: Crear hoja de vida completa
        print("PRUEBA 5: CREAR HOJA DE VIDA COMPLETA")
        print("-" * 70)
        
        codigo = input("Ingrese código de matrícula (6-10 caracteres): ").strip()
        estado_salud = input("Ingrese estado de salud: ").strip()
        
        if not codigo or not estado_salud:
            print("✗ Campos obligatorios vacíos. Prueba cancelada.")
            return
        
        datos_completos = {
            "codigo_matricula": codigo,
            "estado_salud": estado_salud,
            "alergias": ["Ninguna conocida"],
            "tratamientos": [],
            "necesidades_educativas": []
        }
        
        # Validar primero
        formato_correcto, campos_error, errores = servicio_hoja_vida.validar_formato_datos(datos_completos)
        
        if not formato_correcto:
            print("✗ Los datos no pasaron la validación:")
            for campo, error in errores.items():
                print(f"  • {error}")
            return
        
        print("✓ Validación exitosa")
        print()
        
        # Confirmar
        confirmar = input("¿Confirma que desea crear la hoja de vida? (s/n): ").strip().lower()
        
        if confirmar != 's':
            print("Operación cancelada")
            return
        
        # PASO 15: Crear hoja de vida
        print("\nCreando hoja de vida...")
        
        # Usar ID de usuario de prueba (1 = admin por defecto)
        id_usuario_creador = 1
        
        exito, mensaje = servicio_hoja_vida.crear_estudiante_y_hoja_vida(
            id_aspirante,
            datos_completos,
            id_usuario_creador
        )
        
        if exito:
            print(f"✓ {mensaje}")
            print()
            print("REGISTRO CREADO:")
            print(f"  - Estudiante ID: {id_aspirante}")
            print(f"  - Código matrícula: {codigo}")
            print(f"  - Estado salud: {estado_salud}")
        else:
            print(f"✗ Error: {mensaje}")
    
    elif opcion == "6":
        print("Saliendo...")
    else:
        print("Opción no válida")
    
    print()
    print("=" * 70)
    print("TEST COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_cu19_crear_hoja_vida()
    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n✗ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
