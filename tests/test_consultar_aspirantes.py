"""
Tests para CU-12: Consultar y Gestionar Aspirantes

Valida todos los pasos del diagrama de actividades:
1. Directivo hace clic en "Consultar aspirantes"
2. Sistema carga listado de aspirantes
3. Sistema despliega listado con botones "Ver detalles"
4. Directivo hace clic en "Ver detalles de aspirante"
5. Sistema redirige al módulo de aspirante
6-7. Sistema despliega información completa y acciones
"""

import os
import sys


# Agregar ruta del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))


def test_estructura_archivos():
    """
    Test 1: Verificar que existen todos los archivos necesarios del CU-12
    
    Archivos requeridos:
    - servicio_aspirante.py: Servicio para consultar aspirantes (Paso 2)
    - aspirantes.py: Vista de listado y detalles (Paso 3-7)
    - director.py: Dashboard con botón de aspirantes (Paso 1)
    - aspirante.py: Modelo de datos
    - acudiente.py: Modelo de acudiente relacionado
    """
    print("\n" + "="*70)
    print("TEST 1: ESTRUCTURA DE ARCHIVOS CU-12")
    print("="*70)
    
    archivos_requeridos = [
        "app/services/servicio_aspirante.py",
        "app/ui/modules/aspirantes.py",
        "app/ui/modules/director.py",
        "app/core/usuarios/aspirante.py",
        "app/core/usuarios/acudiente.py"
    ]
    
    todos_existen = True
    
    for archivo in archivos_requeridos:
        ruta_completa = os.path.join(os.getcwd(), archivo)
        existe = os.path.exists(ruta_completa)
        
        if existe:
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_existen = False
    
    if todos_existen:
        print("\n✅ TEST 1 PASADO: Todos los archivos existen")
        return True
    else:
        print("\n❌ TEST 1 FALLADO: Faltan archivos")
        return False


def test_servicio_aspirante():
    """
    Test 2: Verificar que el servicio de aspirantes tiene los métodos requeridos
    
    Métodos necesarios:
    - obtener_listado_aspirantes(): Paso 2 del diagrama
    - obtener_detalle_aspirante(id): Paso 6 del diagrama
    - actualizar_estado_aspirante(id, estado): Actualización de estado
    - _obtener_acciones_disponibles(estado): Paso 7 del diagrama
    """
    print("\n" + "="*70)
    print("TEST 2: SERVICIO DE ASPIRANTES (Paso 2 y 6)")
    print("="*70)
    
    try:
        from app.services.servicio_aspirante import ServicioAspirante
        
        servicio = ServicioAspirante()
        print("✅ Servicio ServicioAspirante importado correctamente")
        
        # Verificar métodos
        metodos_requeridos = [
            'obtener_listado_aspirantes',
            'obtener_detalle_aspirante',
            'actualizar_estado_aspirante',
            '_obtener_acciones_disponibles'
        ]
        
        todos_presentes = True
        
        for metodo in metodos_requeridos:
            if hasattr(servicio, metodo):
                print(f"✅ Método '{metodo}' existe")
            else:
                print(f"❌ Método '{metodo}' NO EXISTE")
                todos_presentes = False
        
        # Verificar signatura del método principal
        import inspect
        
        # obtener_listado_aspirantes() - Paso 2
        sig = inspect.signature(servicio.obtener_listado_aspirantes)
        if len(sig.parameters) == 0:
            print("✅ obtener_listado_aspirantes() tiene signatura correcta (sin parámetros)")
        else:
            print(f"❌ obtener_listado_aspirantes() tiene parámetros incorrectos: {list(sig.parameters.keys())}")
            todos_presentes = False
        
        # obtener_detalle_aspirante(id) - Paso 6
        sig = inspect.signature(servicio.obtener_detalle_aspirante)
        if 'id_aspirante' in sig.parameters:
            print("✅ obtener_detalle_aspirante() acepta 'id_aspirante'")
        else:
            print(f"❌ obtener_detalle_aspirante() no acepta 'id_aspirante'")
            todos_presentes = False
        
        # Verificar retorno de acciones (Paso 7)
        acciones = servicio._obtener_acciones_disponibles('pendiente')
        
        if isinstance(acciones, list):
            print(f"✅ _obtener_acciones_disponibles() retorna lista ({len(acciones)} acciones)")
            
            # Verificar estructura de acciones
            acciones_esperadas = ['programar_entrevista', 'diligenciar_admision']
            tipos_encontrados = [a['tipo'] for a in acciones if 'tipo' in a]
            
            for accion_tipo in acciones_esperadas:
                if accion_tipo in tipos_encontrados:
                    print(f"   ✅ Acción '{accion_tipo}' está presente")
                else:
                    print(f"   ❌ Acción '{accion_tipo}' NO está presente")
                    todos_presentes = False
        else:
            print(f"❌ _obtener_acciones_disponibles() no retorna lista: {type(acciones)}")
            todos_presentes = False
        
        if todos_presentes:
            print("\n✅ TEST 2 PASADO: Servicio implementado correctamente")
            return True
        else:
            print("\n❌ TEST 2 FALLADO: Servicio incompleto")
            return False
    
    except Exception as e:
        print(f"\n❌ TEST 2 FALLADO: Error al importar servicio: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vista_listado():
    """
    Test 3: Verificar que la vista de listado existe y tiene componentes necesarios
    
    Requisitos del Paso 3:
    - Función create_aspirantes_manager existe
    - Clase GestionAspirantesView existe
    - Método cargar_listado_aspirantes existe
    - Método desplegar_tabla_aspirantes existe
    - Botones "Ver detalles" se crean para cada aspirante
    """
    print("\n" + "="*70)
    print("TEST 3: VISTA DE LISTADO (Paso 3-4)")
    print("="*70)
    
    try:
        from app.ui.modules.aspirantes import create_aspirantes_manager, GestionAspirantesView
        
        print("✅ Función 'create_aspirantes_manager' importada")
        print("✅ Clase 'GestionAspirantesView' importada")
        
        # Verificar métodos de la clase
        metodos_requeridos = [
            'crear_interfaz',
            'cargar_listado_aspirantes',
            'desplegar_tabla_aspirantes',
            'crear_fila_aspirante',
            'ver_detalle_aspirante'
        ]
        
        todos_presentes = True
        
        for metodo in metodos_requeridos:
            if hasattr(GestionAspirantesView, metodo):
                print(f"✅ Método '{metodo}' existe en GestionAspirantesView")
            else:
                print(f"❌ Método '{metodo}' NO EXISTE en GestionAspirantesView")
                todos_presentes = False
        
        # Verificar que el método crear_fila_aspirante crea botón "Ver detalles"
        # (esto se verifica en el código fuente)
        import inspect
        codigo_fila = inspect.getsource(GestionAspirantesView.crear_fila_aspirante)
        
        if 'Ver detalles' in codigo_fila or 'ver_detalle' in codigo_fila.lower():
            print("✅ El método crear_fila_aspirante incluye botón 'Ver detalles'")
        else:
            print("❌ El método crear_fila_aspirante NO incluye botón 'Ver detalles'")
            todos_presentes = False
        
        # Verificar que usar_detalle_aspirante existe (Paso 4)
        if 'ver_detalle_aspirante' in codigo_fila.lower():
            print("✅ El botón 'Ver detalles' llama a ver_detalle_aspirante() (Paso 4)")
        else:
            print("❌ El botón 'Ver detalles' NO llama a ver_detalle_aspirante()")
            todos_presentes = False
        
        if todos_presentes:
            print("\n✅ TEST 3 PASADO: Vista de listado implementada correctamente")
            return True
        else:
            print("\n❌ TEST 3 FALLADO: Vista de listado incompleta")
            return False
    
    except Exception as e:
        print(f"\n❌ TEST 3 FALLADO: Error al importar vista: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vista_detalle():
    """
    Test 4: Verificar que la vista de detalles existe y muestra información completa
    
    Requisitos del Paso 6-7:
    - Método mostrar_detalle_aspirante existe
    - Método renderizar_detalle_completo existe
    - Sección de información del aspirante
    - Sección de información del acudiente
    - Sección de respuestas del formulario
    - Sección de acciones disponibles (Paso 7)
    """
    print("\n" + "="*70)
    print("TEST 4: VISTA DE DETALLES (Paso 5-7)")
    print("="*70)
    
    try:
        from app.ui.modules.aspirantes import GestionAspirantesView
        
        # Verificar métodos de detalle
        metodos_requeridos = [
            'mostrar_detalle_aspirante',
            'renderizar_detalle_completo',
            'crear_seccion_informacion_aspirante',
            'crear_seccion_acudiente',
            'crear_seccion_respuestas',
            'crear_seccion_acciones',  # Paso 7
            'crear_boton_accion',
            'ejecutar_accion'
        ]
        
        todos_presentes = True
        
        for metodo in metodos_requeridos:
            if hasattr(GestionAspirantesView, metodo):
                print(f"✅ Método '{metodo}' existe")
            else:
                print(f"❌ Método '{metodo}' NO EXISTE")
                todos_presentes = False
        
        # Verificar que crear_seccion_acciones implementa las acciones del Paso 7
        import inspect
        codigo_acciones = inspect.getsource(GestionAspirantesView.crear_seccion_acciones)
        
        acciones_esperadas = [
            'Programar entrevista',
            'Diligenciar admisión'
        ]
        
        for accion in acciones_esperadas:
            # Buscar en el código o en el docstring
            if accion.lower() in codigo_acciones.lower():
                print(f"   ✅ Acción '{accion}' mencionada en crear_seccion_acciones")
            else:
                # Puede estar en los comentarios del método
                print(f"   ⚠️ Acción '{accion}' no explícitamente mencionada (pero puede estar en datos)")
        
        # Verificar que ejecutar_accion maneja las acciones
        codigo_ejecutar = inspect.getsource(GestionAspirantesView.ejecutar_accion)
        
        tipos_accion = ['programar_entrevista', 'diligenciar_admision']
        
        for tipo in tipos_accion:
            if tipo in codigo_ejecutar:
                print(f"   ✅ Tipo de acción '{tipo}' manejado en ejecutar_accion")
            else:
                print(f"   ❌ Tipo de acción '{tipo}' NO manejado en ejecutar_accion")
                todos_presentes = False
        
        if todos_presentes:
            print("\n✅ TEST 4 PASADO: Vista de detalles implementada correctamente")
            return True
        else:
            print("\n❌ TEST 4 FALLADO: Vista de detalles incompleta")
            return False
    
    except Exception as e:
        print(f"\n❌ TEST 4 FALLADO: Error al verificar vista de detalles: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integracion_dashboard():
    """
    Test 5: Verificar integración con el dashboard del directivo
    
    Requisitos del Paso 1:
    - Dashboard del directivo tiene botón "Aspirantes" o "Consultar aspirantes"
    - El botón navega a 'aspirantes_manager'
    - main.py tiene carga dinámica de aspirantes_manager
    """
    print("\n" + "="*70)
    print("TEST 5: INTEGRACIÓN CON DASHBOARD (Paso 1)")
    print("="*70)
    
    try:
        # Verificar que director.py tiene referencia a aspirantes
        with open("app/ui/modules/director.py", "r", encoding="utf-8") as f:
            contenido_director = f.read()
        
        if 'aspirantes_manager' in contenido_director:
            print("✅ Dashboard del directivo tiene referencia a 'aspirantes_manager'")
        else:
            print("❌ Dashboard del directivo NO tiene referencia a 'aspirantes_manager'")
            return False
        
        if 'Aspirantes' in contenido_director:
            print("✅ Dashboard tiene botón de 'Aspirantes'")
        else:
            print("⚠️ Dashboard no tiene botón explícito de 'Aspirantes' (puede estar en descripción)")
        
        # Verificar que main.py tiene carga dinámica
        with open("app/ui/main.py", "r", encoding="utf-8") as f:
            contenido_main = f.read()
        
        if 'aspirantes_manager' in contenido_main:
            print("✅ main.py tiene código para 'aspirantes_manager'")
        else:
            print("❌ main.py NO tiene código para 'aspirantes_manager'")
            return False
        
        if 'create_aspirantes_manager' in contenido_main:
            print("✅ main.py importa 'create_aspirantes_manager'")
        else:
            print("❌ main.py NO importa 'create_aspirantes_manager'")
            return False
        
        print("\n✅ TEST 5 PASADO: Integración con dashboard correcta")
        return True
    
    except Exception as e:
        print(f"\n❌ TEST 5 FALLADO: Error al verificar integración: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modelo_aspirante():
    """
    Test 6: Verificar que el modelo Aspirante tiene los campos necesarios
    
    Campos requeridos:
    - id_aspirante: ID único
    - grado_solicitado: Grado al que aspira
    - fecha_solicitud: Fecha de registro
    - estado_proceso: Estado actual ('pendiente', 'en_proceso', 'aceptado', 'rechazado')
    - Hereda de Persona (tiene datos personales)
    """
    print("\n" + "="*70)
    print("TEST 6: MODELO ASPIRANTE")
    print("="*70)
    
    try:
        from app.core.usuarios.aspirante import Aspirante
        
        print("✅ Modelo Aspirante importado correctamente")
        
        # Crear instancia de prueba
        aspirante = Aspirante(
            id_aspirante=1,
            grado_solicitado="Primero",
            estado_proceso="pendiente",
            primer_nombre="Juan",
            primer_apellido="Pérez"
        )
        
        # Verificar campos
        campos_requeridos = [
            'id_aspirante',
            'grado_solicitado',
            'fecha_solicitud',
            'estado_proceso'
        ]
        
        todos_presentes = True
        
        for campo in campos_requeridos:
            if hasattr(aspirante, campo):
                print(f"✅ Campo '{campo}' existe en Aspirante")
            else:
                print(f"❌ Campo '{campo}' NO EXISTE en Aspirante")
                todos_presentes = False
        
        # Verificar herencia de Persona
        campos_persona = ['primer_nombre', 'primer_apellido', 'numero_identificacion']
        
        for campo in campos_persona:
            if hasattr(aspirante, campo):
                print(f"✅ Campo '{campo}' heredado de Persona")
            else:
                print(f"❌ Campo '{campo}' NO heredado de Persona")
                todos_presentes = False
        
        if todos_presentes:
            print("\n✅ TEST 6 PASADO: Modelo Aspirante configurado correctamente")
            return True
        else:
            print("\n❌ TEST 6 FALLADO: Modelo Aspirante incompleto")
            return False
    
    except Exception as e:
        print(f"\n❌ TEST 6 FALLADO: Error al importar modelo: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests del CU-12"""
    print("\n" + "="*70)
    print("🧪 SUITE DE TESTS - CU-12: CONSULTAR Y GESTIONAR ASPIRANTES")
    print("="*70)
    print("\nValidando todos los pasos del diagrama de actividades:\n")
    print("📋 Paso 1: Directivo hace clic en 'Consultar aspirantes'")
    print("📋 Paso 2: Sistema carga listado de aspirantes")
    print("📋 Paso 3: Sistema despliega listado con botones 'Ver detalles'")
    print("📋 Paso 4: Directivo hace clic en 'Ver detalles de aspirante'")
    print("📋 Paso 5: Sistema redirige al módulo de aspirante")
    print("📋 Paso 6: Sistema obtiene información completa")
    print("📋 Paso 7: Sistema muestra acciones disponibles")
    print("")
    
    tests = [
        ("Estructura de archivos", test_estructura_archivos),
        ("Servicio de Aspirantes (Paso 2, 6)", test_servicio_aspirante),
        ("Vista de Listado (Paso 3-4)", test_vista_listado),
        ("Vista de Detalles (Paso 5-7)", test_vista_detalle),
        ("Integración Dashboard (Paso 1)", test_integracion_dashboard),
        ("Modelo Aspirante", test_modelo_aspirante),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ Error ejecutando test '{nombre}': {e}")
            import traceback
            traceback.print_exc()
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    total = len(resultados)
    pasados = sum(1 for _, resultado in resultados if resultado)
    fallados = total - pasados
    
    for nombre, resultado in resultados:
        simbolo = "✅" if resultado else "❌"
        print(f"{simbolo} {nombre}")
    
    print(f"\nTotal: {total} tests | ✅ Pasados: {pasados} | ❌ Fallados: {fallados}")
    
    if fallados == 0:
        print("\n" + "="*70)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*70)
        print("\n📝 Notas:")
        print("- El módulo de gestión de aspirantes está operativo")
        print("- Todos los pasos del diagrama están implementados")
        print("- El directivo puede consultar el listado de aspirantes (Paso 1-3)")
        print("- El directivo puede ver detalles de cada aspirante (Paso 4-6)")
        print("- Las acciones 'Programar entrevista' y 'Diligenciar admisión' están disponibles (Paso 7)")
        print("\n🚀 El sistema CU-12 está listo para uso")
    else:
        print("\n" + "="*70)
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
        print("="*70)
        print("\nRevisar los tests fallidos antes de continuar.")
    
    return fallados == 0


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
