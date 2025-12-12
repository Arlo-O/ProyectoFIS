"""
Test del CU-18: Admitir Aspirante
Verifica el funcionamiento del servicio de admisión
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.services.servicio_admision import ServicioAdmision
from app.services.servicio_aspirante import ServicioAspirante


def test_cu18_admitir_aspirante():
    """
    Prueba el flujo completo del CU-18
    """
    print("=" * 70)
    print("TEST CU-18: ADMITIR ASPIRANTE")
    print("=" * 70)
    print()
    
    # Inicializar servicios
    servicio_aspirante = ServicioAspirante()
    servicio_admision = ServicioAdmision()
    
    # PASO 1: Obtener listado de aspirantes
    print("PASO 1: Obteniendo listado de aspirantes...")
    exito, aspirantes, mensaje = servicio_aspirante.obtener_listado_aspirantes()
    
    if not exito or not aspirantes:
        print(f"✗ No hay aspirantes disponibles para probar: {mensaje}")
        return
    
    print(f"✓ Se encontraron {len(aspirantes)} aspirantes")
    print()
    
    # PASO 2: Mostrar aspirantes disponibles
    print("Aspirantes disponibles:")
    print("-" * 70)
    for i, asp in enumerate(aspirantes[:5], 1):  # Mostrar solo los primeros 5
        print(f"{i}. ID: {asp['id_aspirante']:3} | {asp['nombre_completo']:30} | Estado: {asp['estado_proceso']}")
    print()
    
    # PASO 3: Buscar un aspirante en estado pendiente o en_proceso
    aspirante_prueba = None
    for asp in aspirantes:
        if asp['estado_proceso'] in ['pendiente', 'en_proceso']:
            aspirante_prueba = asp
            break
    
    if not aspirante_prueba:
        print("✗ No hay aspirantes en estado 'pendiente' o 'en_proceso' para probar")
        print("  Cree un aspirante mediante preinscripción primero")
        return
    
    print(f"ASPIRANTE SELECCIONADO PARA PRUEBA:")
    print(f"  ID: {aspirante_prueba['id_aspirante']}")
    print(f"  Nombre: {aspirante_prueba['nombre_completo']}")
    print(f"  Estado actual: {aspirante_prueba['estado_proceso']}")
    print()
    
    # PASO 4: Probar verificación de estado
    print("PASO 4: Verificando estado del aspirante...")
    exito, estado, justif = servicio_admision.verificar_estado_aspirante(
        aspirante_prueba['id_aspirante']
    )
    
    if exito:
        print(f"✓ Estado verificado: {estado}")
        if justif:
            print(f"  Justificación existente: {justif}")
    else:
        print(f"✗ Error al verificar estado: {justif}")
    print()
    
    # PASO 5: Menú de opciones
    print("=" * 70)
    print("OPCIONES DE PRUEBA:")
    print("=" * 70)
    print("1. Admitir aspirante")
    print("2. Rechazar aspirante (con justificación)")
    print("3. Intentar rechazar sin justificación (debe fallar)")
    print("4. Salir sin cambios")
    print()
    
    opcion = input("Seleccione una opción (1-4): ").strip()
    print()
    
    if opcion == "1":
        # PRUEBA: ADMITIR ASPIRANTE
        print("PRUEBA: ADMITIR ASPIRANTE")
        print("-" * 70)
        confirmar = input(f"¿Confirma que desea ADMITIR a '{aspirante_prueba['nombre_completo']}'? (s/n): ").strip().lower()
        
        if confirmar == 's':
            print("\nLlamando a servicio_admision.admitir_aspirante()...")
            exito, mensaje = servicio_admision.admitir_aspirante(
                aspirante_prueba['id_aspirante']
            )
            
            if exito:
                print(f"✓ {mensaje}")
                print(f"  Estado actualizado a: admitido")
            else:
                print(f"✗ Error: {mensaje}")
        else:
            print("Operación cancelada")
    
    elif opcion == "2":
        # PRUEBA: RECHAZAR ASPIRANTE
        print("PRUEBA: RECHAZAR ASPIRANTE")
        print("-" * 70)
        justificacion = input("Ingrese la justificación del rechazo: ").strip()
        
        if not justificacion:
            print("✗ Error: La justificación no puede estar vacía")
        else:
            confirmar = input(f"\n¿Confirma que desea RECHAZAR a '{aspirante_prueba['nombre_completo']}'? (s/n): ").strip().lower()
            
            if confirmar == 's':
                print("\nLlamando a servicio_admision.rechazar_aspirante()...")
                exito, mensaje = servicio_admision.rechazar_aspirante(
                    aspirante_prueba['id_aspirante'],
                    justificacion
                )
                
                if exito:
                    print(f"✓ {mensaje}")
                    print(f"  Estado actualizado a: rechazado")
                    print(f"  Justificación: {justificacion}")
                else:
                    print(f"✗ Error: {mensaje}")
            else:
                print("Operación cancelada")
    
    elif opcion == "3":
        # PRUEBA: RECHAZAR SIN JUSTIFICACIÓN (DEBE FALLAR)
        print("PRUEBA: RECHAZAR SIN JUSTIFICACIÓN (Validación)")
        print("-" * 70)
        print("Intentando rechazar sin proporcionar justificación...")
        
        exito, mensaje = servicio_admision.rechazar_aspirante(
            aspirante_prueba['id_aspirante'],
            ""  # Justificación vacía
        )
        
        if not exito:
            print(f"✓ Validación correcta: {mensaje}")
            print("  El sistema rechazó correctamente la operación sin justificación")
        else:
            print(f"✗ Error: El sistema permitió rechazar sin justificación (no debería)")
    
    elif opcion == "4":
        print("Saliendo sin realizar cambios...")
    else:
        print("Opción no válida")
    
    print()
    print("=" * 70)
    print("TEST COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_cu18_admitir_aspirante()
    except KeyboardInterrupt:
        print("\n\nPrueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n✗ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
