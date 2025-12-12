# Diagrama de Secuencia UML: CU-12 - Consultar y Gestionar Aspirantes

**Versión**: 1.0 - Notación UML 2.5  
**Fecha**: 12 de Diciembre 2025  
**Basado en**: OMG Unified Modeling Language™ (OMG UML) Version 2.5  
**Caso de Uso**: CU-12 - Consultar y Gestionar Aspirantes

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Descripción del Caso de Uso](#descripción-del-caso-de-uso)
3. [Participantes del Diagrama](#participantes-del-diagrama)
4. [Fases del Proceso](#fases-del-proceso)
5. [Elementos UML Utilizados](#elementos-uml-utilizados)
6. [Flujo Detallado](#flujo-detallado)
7. [Consultas a Base de Datos](#consultas-a-base-de-datos)
8. [Trazas de Ocurrencias](#trazas-de-ocurrencias)
9. [Estados del Sistema](#estados-del-sistema)
10. [Cómo Visualizar](#cómo-visualizar)
11. [Referencias](#referencias)

---

## Introducción

### Propósito del Diagrama

Este diagrama de secuencia modela **el flujo completo del caso de uso CU-12: Consultar y Gestionar Aspirantes**, desde que el Directivo hace clic en el botón de acceso hasta que visualiza los detalles completos de un aspirante específico.

### Alcance

El diagrama captura:
- ✅ **Paso 1**: Directivo hace clic en "Consultar aspirantes"
- ✅ **Paso 2**: Sistema carga listado aspirantes actuales
- ✅ **Paso 3**: Sistema despliega listado aspirantes
- ✅ **Paso 4**: Directivo hace clic en "Ver detalles de aspirante"
- ✅ **Paso 5**: Sistema redirige al módulo de aspirante
- ✅ **Paso 6-7**: Sistema despliega información completa y acciones disponibles

### Actores Involucrados

| Actor | Rol | Acciones |
|-------|-----|----------|
| **Directivo** | Usuario del sistema con rol administrativo | - Hace clic en botón "Aspirantes"<br>- Consulta listado<br>- Hace clic en "Ver detalles" |

---

## Descripción del Caso de Uso

### CU-12: Consultar y Gestionar Aspirantes

**Objetivo**: Permitir al directivo consultar el listado de aspirantes registrados en el sistema y acceder a los detalles individuales de cada uno.

### Flujo Normal

1. **Directivo** hace clic en el botón "📋 Aspirantes" en su dashboard
2. **Sistema** carga el listado de aspirantes desde la base de datos
3. **Sistema** despliega una tabla con todos los aspirantes mostrando:
   - Nombre completo
   - Identificación
   - Grado solicitado
   - Fecha de solicitud
   - Estado del proceso
   - Botón "Ver detalles"
4. **Directivo** hace clic en "Ver detalles" de un aspirante específico
5. **Sistema** redirige a la vista de detalle del aspirante
6. **Sistema** carga información completa del aspirante y su acudiente
7. **Sistema** muestra información detallada y acciones disponibles según el estado

### Precondiciones

- ✅ Directivo autenticado en el sistema
- ✅ Dashboard del directivo cargado
- ✅ Base de datos con tabla `aspirante` y `persona` disponibles

### Postcondiciones

- ✅ Listado de aspirantes desplegado o mensaje si no hay registros
- ✅ Detalle completo de aspirante mostrado (si se selecciona uno)
- ✅ Acciones disponibles según estado del aspirante

---

## Participantes del Diagrama

### Tabla de Participantes

| # | Participante | Tipo | Responsabilidad |
|---|--------------|------|-----------------|
| 1 | `Directivo` | Actor | Inicia el proceso y selecciona aspirantes |
| 2 | `director_dashboard` | Frame | Dashboard con botones de navegación |
| 3 | `app.ui.main` | Módulo | Controlador principal de UI |
| 4 | `show_frame()` | Función | Gestiona visibilidad de frames |
| 5 | `app.ui.modules.aspirantes` | Módulo | Contiene lógica de la vista de aspirantes |
| 6 | `create_aspirantes_manager()` | Función | Factory que crea la vista |
| 7 | `main_frame` | Frame | Contenedor principal |
| 8 | `GestionAspirantesView` | Clase | Vista principal de gestión |
| 9 | `crear_interfaz()` | Método | Construye la interfaz |
| 10 | `cargar_listado_aspirantes()` | Método | Carga datos desde servicio |
| 11 | `ServicioAspirante` | Clase | Servicio de lógica de negocio |
| 12 | `obtener_listado_aspirantes()` | Método | Consulta BD para listado |
| 13 | `PostgreSQL` | Base de Datos | Almacena información |
| 14 | `desplegar_tabla_aspirantes()` | Método | Renderiza tabla |
| 15 | `Canvas + Scrollbar` | Widget | Canvas scrollable para tabla |
| 16 | `crear_fila_aspirante()` | Método | Crea cada fila de la tabla |
| 17 | `Button 'Ver detalles'` | Widget | Botón en cada fila |
| 18 | `ver_detalle_aspirante()` | Método | Maneja clic en botón |
| 19 | `mostrar_detalle_aspirante()` | Método | Muestra vista de detalle |
| 20 | `obtener_detalle_aspirante()` | Método | Consulta BD para detalle |
| 21 | `renderizar_detalle_completo()` | Método | Renderiza vista de detalle |

### Clasificación por Capa

| Capa | Participantes |
|------|---------------|
| **Presentación (UI)** | director_dashboard, GestionAspirantesView, crear_interfaz(), desplegar_tabla_aspirantes(), crear_fila_aspirante(), renderizar_detalle_completo(), Canvas, Button |
| **Control** | app.ui.main, show_frame(), create_aspirantes_manager(), ver_detalle_aspirante(), mostrar_detalle_aspirante() |
| **Lógica de Negocio** | ServicioAspirante, obtener_listado_aspirantes(), obtener_detalle_aspirante() |
| **Datos** | PostgreSQL |

---

## Fases del Proceso

### FASE 1: Directivo Accede al Módulo

**Mensajes**: [01] - [06]

**Descripción**: El directivo hace clic en el botón "Aspirantes" en su dashboard, lo que desencadena la navegación al módulo de aspirantes.

**Flujo**:
```
Directivo → dashboard → uimain → show_frame('aspirantes_manager')
```

**Estado Inicial**:
- Dashboard del directivo visible
- Frames disponibles: {login, director_dashboard, ...}
- `aspirantes_manager` NO existe en frames

**Estado Final**:
- show_frame() detecta que frame no existe
- Se prepara para carga dinámica

---

### FASE 2: Carga Dinámica del Módulo

**Mensajes**: [07] - [15]

**Descripción**: El sistema carga dinámicamente el módulo de aspirantes, crea la instancia de la vista y el servicio.

**Flujo**:
```
show_frame → importa aspmodule → create_aspirantes_manager() → 
GestionAspirantesView() → ServicioAspirante()
```

**Acciones**:
1. Importa módulo `app.ui.modules.aspirantes`
2. Obtiene referencia a `main_frame`
3. Llama a función factory `create_aspirantes_manager()`
4. Crea Frame contenedor
5. Instancia `GestionAspirantesView`
6. Constructor inicializa:
   - `self.servicio = ServicioAspirante()`
   - `self.aspirantes_actuales = []`
   - `self.detalle_actual = None`

**Estado Final**:
- Módulo cargado en memoria
- Vista instanciada
- Servicio listo para consultas

---

### FASE 3: Construcción de la Interfaz

**Mensajes**: [16] - [24]

**Descripción**: El método `crear_interfaz()` construye todos los elementos visuales de la pantalla de listado.

**Componentes Creados**:

```
┌──────────────────────────────────────┐
│ 📋 Gestión de Aspirantes  [🔄][←]   │ ← Header
│ Consulte y gestione los aspirantes   │ ← Descripción
├──────────────────────────────────────┤
│ [contenedor_tabla]                   │ ← Contenedor vacío
│                                      │   (se llenará en Fase 4)
└──────────────────────────────────────┘
```

**Widgets**:
- **Header Frame**: Contiene título y botones
  - Label "📋 Gestión de Aspirantes"
  - Button "🔄 Actualizar"
  - Button "← Volver al Dashboard"
- **Label descripción**: Texto informativo
- **Contenedor tabla**: Frame blanco donde irá la tabla

**Estado Final**:
- Interfaz estructural creada
- Listo para cargar datos

---

### FASE 4: Consulta a la Base de Datos

**Mensajes**: [25] - [51]

**Descripción**: El sistema consulta la base de datos para obtener todos los aspirantes registrados.

**Sub-fases**:

#### 4.1: Preparación
- Limpia contenedor_tabla
- Muestra indicador "⏳ Cargando aspirantes..."

#### 4.2: Consulta SQL
```sql
SELECT 
    a.id_aspirante,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.tipo_identificacion,
    p.numero_identificacion,
    p.fecha_nacimiento,
    p.genero,
    p.direccion,
    p.telefono,
    a.grado_solicitado,
    a.fecha_solicitud,
    a.estado_proceso
FROM aspirante a
INNER JOIN persona p ON a.id_aspirante = p.id_persona
ORDER BY a.fecha_solicitud DESC
```

#### 4.3: Procesamiento (Loop)
Para cada registro:
1. Construye `nombre_completo` concatenando nombres y apellidos
2. Calcula `edad` desde `fecha_nacimiento`
3. Formatea fechas a formato "DD/MM/YYYY"
4. Crea diccionario `aspirante_dict` con todos los campos
5. Agrega a lista `aspirantes`

**Campos del diccionario**:
```python
{
    'id_aspirante': int,
    'nombre_completo': str,
    'primer_nombre': str,
    'segundo_nombre': str,
    'primer_apellido': str,
    'segundo_apellido': str,
    'tipo_identificacion': str,
    'numero_identificacion': str,
    'grado_solicitado': str,
    'fecha_solicitud': str,
    'estado_proceso': str,
    'edad': int,
    'genero': str,
    'direccion': str,
    'telefono': str
}
```

**Casos Especiales**:

**Fragmento `opt` - Sin aspirantes**:
```plantuml
opt aspirantes == []
    mostrar "📭 No hay aspirantes registrados"
    return
end
```

**Fragmento `opt` - Error**:
```plantuml
opt exito == False
    mostrar "❌ Error al consultar aspirantes"
    return
end
```

**Estado Final**:
- Lista `self.aspirantes_actuales` poblada
- Listo para renderizar tabla

---

### FASE 5: Renderizado de la Tabla

**Mensajes**: [52] - [76]

**Descripción**: El sistema crea la tabla visual con todos los aspirantes usando Canvas scrollable.

**Estructura**:

```
┌────────────────────────────────────────────────────┐
│ # │ Nombre Completo │ ID │ Grado │ Fecha │ Estado │ ● │ ← Encabezados
├────────────────────────────────────────────────────┤
│ 1 │ Juan Pérez      │ TI │ 1°    │ 01/12 │ Pend.  │👁️│ ← Fila 1
│ 2 │ María García    │ TI │ 2°    │ 28/11 │ Acept. │👁️│ ← Fila 2
│ 3 │ Pedro Martínez  │ CC │ 1°    │ 25/11 │ EnProc │👁️│ ← Fila 3
├────────────────────────────────────────────────────┤
│ Total de aspirantes: 3                             │ ← Footer
└────────────────────────────────────────────────────┘
         ↑↓ Scrollbar vertical
```

**Componentes**:

1. **Canvas + Scrollbar**: Permite scroll vertical
2. **scrollable_frame**: Frame interno al Canvas
3. **header_frame**: Frame con encabezados en color `COLOR_HEADER_PRE`
4. **Fragmento `loop`**: Para cada aspirante
   ```plantuml
   loop para cada aspirante en self.aspirantes_actuales
       crear_fila_aspirante(scrollable_frame, idx, aspirante)
   end
   ```

**Cada fila contiene**:
- Label: Número secuencial
- Label: Nombre completo
- Label: Tipo + Número de identificación
- Label: Grado solicitado
- Label: Fecha de solicitud
- Label: Estado (con color según estado)
- **Button**: "👁️ Ver detalles" con `command=lambda`

**Colores de Estado**:
```python
estado_colors = {
    'pendiente': '#ffc107',     # Amarillo
    'en_proceso': '#17a2b8',    # Azul
    'aceptado': '#28a745',      # Verde
    'rechazado': '#dc3545'      # Rojo
}
```

**Estado Final**:
- Tabla completa renderizada
- Todos los botones funcionales
- Sistema esperando interacción

---

### FASE 6: Mostrar el Frame

**Mensajes**: [77] - [81]

**Descripción**: El frame de aspirantes se hace visible ocultando otros frames.

**Fragmento `loop`**:
```plantuml
loop para cada frame en frames.values()
    other_frame.grid_remove()
end
```

**Acción**:
```python
frame.grid(row=0, column=0, sticky="nsew")
frames['aspirantes_manager'] = frame
```

**Estado Final**:
- Frame de aspirantes visible
- Usuario puede interactuar
- **PUNTO DE ESPERA 1**: Sistema esperando que directivo haga clic

---

### FASE 7: Directivo Hace Clic en "Ver Detalles"

**Mensajes**: [82] - [84]

**Descripción**: El directivo selecciona un aspirante específico haciendo clic en su botón "Ver detalles".

**Flujo**:
```
Directivo → Button → ver_detalle_aspirante(id_aspirante)
```

**Acción**:
1. Botón ejecuta su `command=lambda asp=aspirante: self.ver_detalle_aspirante(asp['id_aspirante'])`
2. Método `ver_detalle_aspirante()` oculta `frame_listado`
3. Llama a `mostrar_detalle_aspirante(id_aspirante)`

**Estado**:
- Listado oculto
- Preparando vista de detalle

---

### FASE 8: Crear Frame de Detalle

**Mensajes**: [85] - [88]

**Descripción**: Se crea o limpia el frame de detalle y se muestra indicador de carga.

**Acciones**:
1. Crear/limpiar `self.frame_detalle`
2. `.pack()` para hacerlo visible
3. Mostrar Label "⏳ Cargando información del aspirante..."
4. Llamar `.update()` para renderizar indicador

**Estado**:
- Frame de detalle visible
- Indicador de carga mostrándose

---

### FASE 9: Obtener Detalle Completo

**Mensajes**: [89] - [105]

**Descripción**: El sistema consulta la base de datos para obtener información completa del aspirante y su acudiente.

**Consulta 1: Datos del Aspirante**

```sql
SELECT 
    a.id_aspirante,
    a.grado_solicitado,
    a.fecha_solicitud,
    a.estado_proceso,
    a.id_acudiente,
    p.tipo_identificacion,
    p.numero_identificacion,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.fecha_nacimiento,
    p.genero,
    p.direccion,
    p.telefono
FROM aspirante a
INNER JOIN persona p ON a.id_aspirante = p.id_persona
WHERE a.id_aspirante = :id_aspirante
```

**Procesamiento**:
- Construye `aspirante_info` (dict)
- Calcula nombre completo y edad
- Formatea fechas

**Fragmento `opt` - Consulta Acudiente**:

```plantuml
opt id_acudiente != None
    consultar acudiente en BD
    construir acudiente_info (dict)
end
```

**Consulta 2: Datos del Acudiente (Condicional)**

```sql
SELECT 
    ac.id_acudiente,
    ac.parentesco,
    ac.email,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.numero_identificacion,
    p.telefono,
    p.direccion
FROM acudiente ac
INNER JOIN persona p ON ac.id_acudiente = p.id_persona
WHERE ac.id_acudiente = :id_acudiente
```

**Estructura del Resultado**:
```python
detalle_completo = {
    'aspirante': {
        'id_aspirante': int,
        'nombre_completo': str,
        'tipo_identificacion': str,
        'numero_identificacion': str,
        'fecha_nacimiento': str,
        'edad': int,
        'genero': str,
        'direccion': str,
        'telefono': str,
        'grado_solicitado': str,
        'fecha_solicitud': str,
        'estado_proceso': str
    },
    'acudiente': {
        'id_acudiente': int,
        'nombre_completo': str,
        'numero_identificacion': str,
        'parentesco': str,
        'email': str,
        'telefono': str,
        'direccion': str
    } or None,
    'acciones_disponibles': [...]
}
```

**Estado Final**:
- `detalle_completo` disponible
- Listo para renderizar

---

### FASE 10: Renderizar Detalle Completo

**Mensajes**: [106] - [115]

**Descripción**: El sistema renderiza toda la información del aspirante en una vista detallada scrollable.

**Estructura Visual**:

```
┌──────────────────────────────────────────────┐
│ 👤 Detalles del Aspirante    [← Volver]     │ ← Header
├──────────────────────────────────────────────┤
│ 📄 INFORMACIÓN DEL ASPIRANTE                 │ ← Sección 1
│ ────────────────────────────────────────────│
│ Nombre completo: Juan Pérez García           │
│ Identificación: TI 123456789                 │
│ Fecha nacimiento: 15/05/2015 (9 años)       │
│ Género: Masculino                            │
│ Dirección: Calle 123 #45-67                  │
│ Teléfono: 3001234567                         │
│ Grado solicitado: Primero                    │
│ Fecha solicitud: 01/12/2025 15:30            │
│ Estado: ● Pendiente                          │
├──────────────────────────────────────────────┤
│ 👨‍👩‍👧 INFORMACIÓN DEL ACUDIENTE                 │ ← Sección 2 (opt)
│ ────────────────────────────────────────────│
│ Nombre: María García Rodríguez               │
│ Identificación: CC 987654321                 │
│ Parentesco: Madre                            │
│ Email: maria.garcia@email.com                │
│ Teléfono: 3009876543                         │
│ Dirección: Calle 123 #45-67                  │
├──────────────────────────────────────────────┤
│ ⚡ ACCIONES DISPONIBLES                       │ ← Sección 3
│ ────────────────────────────────────────────│
│ [Programar entrevista]                       │
│ [Aprobar aspirante]                          │
│ [Rechazar aspirante]                         │
└──────────────────────────────────────────────┘
         ↑↓ Scrollbar vertical
```

**Componentes**:

1. **Canvas + Scrollbar**: Para contenido largo
2. **content_frame**: Frame scrollable
3. **Header**: Título + Botón "Volver"
4. **Sección Aspirante**: `crear_seccion_informacion_aspirante()`
   - Card con todos los datos personales
   - Labels organizados en grid
5. **Fragmento `opt`**: Sección Acudiente (si existe)
   ```plantuml
   opt detalle['acudiente'] != None
       crear_seccion_informacion_acudiente()
   end
   ```
6. **Sección Acciones**: `crear_seccion_acciones()`
   - Botones según `estado_proceso`
   - Colores según tipo de acción

**Acciones Disponibles según Estado**:

| Estado | Acciones |
|--------|----------|
| `pendiente` | - Programar entrevista<br>- Aprobar aspirante<br>- Rechazar aspirante |
| `en_proceso` | - Ver historial<br>- Aprobar aspirante<br>- Rechazar aspirante |
| `aceptado` | - Ver historial<br>- Cambiar a en proceso |
| `rechazado` | - Ver historial<br>- Reactivar aspirante |

**Estado Final**:
- Vista de detalle completamente renderizada
- Información completa visible
- Acciones disponibles según estado
- **PUNTO DE ESPERA 2**: Sistema esperando interacción del directivo

---

## Elementos UML Utilizados

### 1. Actor

**Notación**: `actor Directivo as director`

```
┌────────┐
│  ◉     │ Directivo
│  │     │
│ / \    │
└────────┘
```

**En el diagrama**: Usuario con rol de directivo que inicia y controla el flujo.

---

### 2. Participantes

**Notación**: `participant "<<stereotype>>\nNombre" as alias`

**Estereotipos utilizados**:

| Estereotipo | Descripción | Ejemplos |
|-------------|-------------|----------|
| `<<Frame>>` | Widget Frame de Tkinter | director_dashboard, main_frame |
| `<<module>>` | Módulo Python | app.ui.main, app.ui.modules.aspirantes |
| `<<function>>` | Función standalone | show_frame(), create_aspirantes_manager() |
| `<<class>>` | Clase instanciable | GestionAspirantesView, ServicioAspirante |
| `<<method>>` | Método de clase | crear_interfaz(), cargar_listado_aspirantes() |
| `<<database>>` | Base de datos | PostgreSQL |
| `<<widget>>` | Widget de UI | Canvas, Button |

---

### 3. Mensajes

#### 3.1 Mensaje Síncrono

**Notación**: `A -> B: mensaje`

**Ejemplos**:
- `director -> dashboard: hace clic en botón "📋 Aspirantes"`
- `cargarlist -> servicio: obtener_listado_aspirantes()`

#### 3.2 Mensaje de Retorno

**Notación**: `B --> A: resultado`

**Ejemplos**:
- `database --> obtenerlist: resultados (lista de Row)`
- `servicio --> cargarlist: (exito, aspirantes, mensaje)`

#### 3.3 Mensaje de Creación

**Notación**: `A -> B ** : new B()`

**Ejemplos**:
- `createasp -> mainframe ** : frame = tk.Frame(parent)`
- `createasp -> viewclass ** : view = GestionAspirantesView(...)`
- `desplegarTabla -> canvas ** : crear Canvas + Scrollbar`

---

### 4. Activaciones

**Notación**: `activate participante` / `deactivate participante`

**Representación visual**: Barra vertical en la línea de vida

```
    A           B
    │           │
    │──────────►│
    │           ┌┴┐
    │           │ │ ← Activación
    │           │ │
    │◄──────────│ │
    │           └┬┘
```

**En el diagrama**: Cada llamada a método tiene su activación correspondiente.

---

### 5. Fragmentos Combinados

#### 5.1 Fragmento `opt` (Opcional)

**Uso 1: Sin aspirantes**
```plantuml
opt aspirantes == []
    cargarlist -> cargarlist: mostrar "📭 No hay aspirantes"
    cargarlist --> crearintf: return (mensaje mostrado)
end
```

**Uso 2: Error en consulta**
```plantuml
opt exito == False
    cargarlist -> cargarlist: mostrar error
    cargarlist --> crearintf: return (error mostrado)
end
```

**Uso 3: Acudiente existe**
```plantuml
opt id_acudiente != None
    obtenerdetalle -> database: query acudiente + persona
    obtenerdetalle -> obtenerdetalle: construir acudiente_info (dict)
end
```

**Uso 4: Mostrar sección acudiente**
```plantuml
opt detalle['acudiente'] != None
    renderdetalle -> renderdetalle: crear_seccion_informacion_acudiente()
end
```

#### 5.2 Fragmento `loop` (Iteración)

**Uso 1: Procesar resultados de BD**
```plantuml
loop para cada row en resultados
    obtenerlist -> obtenerlist: construir nombre_completo
    obtenerlist -> obtenerlist: calcular edad
    obtenerlist -> obtenerlist: formatear fechas
    obtenerlist -> obtenerlist: crear aspirante_dict
    obtenerlist -> obtenerlist: aspirantes.append(aspirante_dict)
end
```

**Uso 2: Crear filas de tabla**
```plantuml
loop para cada aspirante en self.aspirantes_actuales
    desplegarTabla -> crearfila: crear_fila_aspirante(...)
    crearfila -> crearfila: crear row_frame
    crearfila -> crearfila: crear Labels (columnas 1-6)
    crearfila -> btndetalle ** : crear Button "Ver detalles"
end
```

**Uso 3: Ocultar frames**
```plantuml
loop para cada frame en frames.values()
    showframe -> mainframe: other_frame.grid_remove()
end
```

---

### 6. Notas

**Ubicaciones**:
- `note over`: Sobre uno o más participantes
- `note right of`: A la derecha de un participante
- `note left of`: A la izquierda de un participante

**Ejemplos**:

```plantuml
note over obtenerlist
  Método del servicio que:
  1. Crea sesión de BD
  2. Ejecuta query SQL
  3. Procesa resultados
  4. Retorna (bool, list, str)
end note

note right
  Query SQL con JOIN:
  SELECT ... FROM aspirante a
  INNER JOIN persona p ...
end note
```

---

### 7. Separadores de Fases

**Notación**: `== Título ==`

**Fases en el diagrama**:
1. `== PASO 1: Directivo Accede al Módulo ==`
2. `== PASO 2: Carga Dinámica del Módulo ==`
3. `== PASO 3: Construcción de la Interfaz ==`
4. `== PASO 4: Consulta a la Base de Datos ==`
5. `== PASO 5: Renderizado de la Tabla ==`
6. `== PASO 6: Mostrar el Frame ==`
7. `== PASO 7: Directivo Hace Clic en "Ver Detalles" ==`
8. `== PASO 8: Crear Frame de Detalle ==`
9. `== PASO 9: Obtener Detalle Completo ==`
10. `== PASO 10: Renderizar Detalle Completo ==`

---

## Flujo Detallado

### Flujo Resumido

```
1. Directivo clic → 
2. Navegar a aspirantes_manager → 
3. Cargar módulo dinámicamente → 
4. Crear vista y servicio → 
5. Construir interfaz → 
6. Consultar BD para listado → 
7. Procesar resultados → 
8. Renderizar tabla → 
9. Mostrar frame → 
10. Esperar clic en "Ver detalles" → 
11. Ocultar listado → 
12. Consultar BD para detalle → 
13. Obtener datos aspirante + acudiente → 
14. Renderizar vista de detalle → 
15. Mostrar información completa
```

### Puntos de Decisión

| Decisión | Condición | Acción Si | Acción No |
|----------|-----------|-----------|-----------|
| Frame existe? | `frame = frames.get('aspirantes_manager')` | Mostrar frame existente | Cargar módulo dinámicamente |
| Consulta exitosa? | `exito == True` | Procesar resultados | Mostrar error |
| Hay aspirantes? | `len(aspirantes) > 0` | Renderizar tabla | Mostrar "No hay aspirantes" |
| Acudiente existe? | `id_acudiente != None` | Consultar acudiente | Continuar sin acudiente |
| Mostrar sección acudiente? | `detalle['acudiente'] != None` | Renderizar sección | Omitir sección |

---

## Consultas a Base de Datos

### Consulta 1: Listado de Aspirantes

**Propósito**: Obtener todos los aspirantes con información básica

**Query**:
```sql
SELECT 
    a.id_aspirante,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.tipo_identificacion,
    p.numero_identificacion,
    p.fecha_nacimiento,
    p.genero,
    p.direccion,
    p.telefono,
    a.grado_solicitado,
    a.fecha_solicitud,
    a.estado_proceso
FROM aspirante a
INNER JOIN persona p ON a.id_aspirante = p.id_persona
ORDER BY a.fecha_solicitud DESC
```

**Tablas involucradas**:
- `aspirante` (a)
- `persona` (p)

**Join**: INNER JOIN por `id_aspirante = id_persona`

**Ordenamiento**: Por `fecha_solicitud` descendente (más recientes primero)

**Resultado**: Lista de `Row` objects

---

### Consulta 2: Detalle de Aspirante

**Propósito**: Obtener información completa de un aspirante específico

**Query**:
```sql
SELECT 
    a.id_aspirante,
    a.grado_solicitado,
    a.fecha_solicitud,
    a.estado_proceso,
    a.id_acudiente,
    p.tipo_identificacion,
    p.numero_identificacion,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.fecha_nacimiento,
    p.genero,
    p.direccion,
    p.telefono
FROM aspirante a
INNER JOIN persona p ON a.id_aspirante = p.id_persona
WHERE a.id_aspirante = :id_aspirante
```

**Parámetros**: `:id_aspirante` (int)

**Resultado**: Un `Row` object o None

---

### Consulta 3: Información de Acudiente (Condicional)

**Propósito**: Obtener información del acudiente asociado

**Query**:
```sql
SELECT 
    ac.id_acudiente,
    ac.parentesco,
    ac.email,
    p.primer_nombre,
    p.segundo_nombre,
    p.primer_apellido,
    p.segundo_apellido,
    p.numero_identificacion,
    p.telefono,
    p.direccion
FROM acudiente ac
INNER JOIN persona p ON ac.id_acudiente = p.id_persona
WHERE ac.id_acudiente = :id_acudiente
```

**Condición**: Solo se ejecuta si `id_acudiente != None`

**Parámetros**: `:id_acudiente` (int)

**Resultado**: Un `Row` object o None

---

### Modelo de Datos

```
┌─────────────┐         ┌──────────────┐
│   persona   │◄────────│   aspirante  │
├─────────────┤         ├──────────────┤
│ id_persona  │         │ id_aspirante │ (FK → persona.id_persona)
│ primer_nom  │         │ grado_solic  │
│ segundo_nom │         │ fecha_solic  │
│ primer_ape  │         │ estado_proc  │
│ segundo_ape │         │ id_acudiente │ (FK → acudiente.id_acudiente)
│ tipo_ident  │         └──────────────┘
│ num_ident   │                │
│ fecha_nac   │                │
│ genero      │                ▼
│ direccion   │         ┌──────────────┐
│ telefono    │         │  acudiente   │
└─────────────┘         ├──────────────┤
        ▲               │ id_acudiente │ (FK → persona.id_persona)
        │               │ parentesco   │
        └───────────────│ email        │
                        └──────────────┘
```

---

## Trazas de Ocurrencias

### Traza Válida: Listado con Aspirantes

```
1. Directivo clic en "Aspirantes"
2. Sistema navega a aspirantes_manager
3. Sistema carga módulo dinámicamente
4. Sistema crea GestionAspirantesView
5. Sistema instancia ServicioAspirante
6. Sistema construye interfaz
7. Sistema consulta BD (query aspirantes)
8. BD retorna 3 aspirantes
9. Sistema procesa cada aspirante (loop x3)
10. Sistema renderiza tabla con 3 filas
11. Sistema muestra frame
12. [ESPERA] Usuario ve listado
```

### Traza Válida: Ver Detalle

```
1. [Continuación desde listado visible]
2. Directivo clic en "Ver detalles" (aspirante #2)
3. Sistema oculta listado
4. Sistema crea frame de detalle
5. Sistema consulta BD (query detalle aspirante)
6. BD retorna datos aspirante
7. Sistema verifica id_acudiente (existe)
8. Sistema consulta BD (query acudiente)
9. BD retorna datos acudiente
10. Sistema construye detalle_completo
11. Sistema renderiza secciones:
    - Información aspirante
    - Información acudiente
    - Acciones disponibles
12. Sistema muestra frame de detalle
13. [ESPERA] Usuario ve detalle completo
```

### Traza Válida: Sin Aspirantes

```
1. Directivo clic en "Aspirantes"
2. Sistema navega a aspirantes_manager
3. Sistema carga módulo dinámicamente
4. Sistema crea vista y servicio
5. Sistema construye interfaz
6. Sistema consulta BD (query aspirantes)
7. BD retorna lista vacía
8. Sistema verifica aspirantes == []
9. Sistema muestra "📭 No hay aspirantes"
10. [ESPERA] Usuario ve mensaje
```

### Traza Inválida: Frame no existe y no se puede cargar

```
❌ 1. Directivo clic en "Aspirantes"
❌ 2. Sistema intenta show_frame('aspirantes_manager')
❌ 3. Frame no existe en frames
❌ 4. Sistema intenta importar módulo
❌ 5. ImportError: módulo no encontrado
❌ 6. Sistema no puede mostrar frame
```

**Prevención**: Verificar que módulo `app.ui.modules.aspirantes` existe antes del despliegue.

### Traza Inválida: Error en BD

```
❌ 1-6. [Igual que traza válida]
❌ 7. Sistema consulta BD
❌ 8. BD retorna error (conexión perdida)
❌ 9. Sistema captura excepción
❌ 10. Sistema muestra mensaje de error
❌ 11. [ESPERA] Usuario ve error, no puede ver aspirantes
```

**Prevención**: Manejo de excepciones con try/except en `obtener_listado_aspirantes()`.

---

## Estados del Sistema

### Estado 1: Inicial

**Antes del clic en "Aspirantes"**

```python
frames = {
    'login': <Frame>,
    'director_dashboard': <Frame>,
    # 'aspirantes_manager' NO EXISTE
}

director_dashboard: VISIBLE
aspirantes_manager: NO EXISTE
```

---

### Estado 2: Después de Carga Dinámica

**Después de crear vista**

```python
frames = {
    'login': <Frame>,
    'director_dashboard': <Frame>,
    'aspirantes_manager': <Frame>  # ✅ CREADO
}

aspirantes_manager.aspirantes_actuales: []  # Vacío
aspirantes_manager.detalle_actual: None
aspirantes_manager.servicio: <ServicioAspirante instance>
aspirantes_manager.frame_listado: <Frame VISIBLE>
aspirantes_manager.frame_detalle: None
```

---

### Estado 3: Después de Cargar Listado

**Después de consulta BD exitosa**

```python
aspirantes_manager.aspirantes_actuales: [
    {'id_aspirante': 1, 'nombre_completo': 'Juan Pérez', ...},
    {'id_aspirante': 2, 'nombre_completo': 'María García', ...},
    {'id_aspirante': 3, 'nombre_completo': 'Pedro Martínez', ...}
]

aspirantes_manager.frame_listado: VISIBLE con tabla renderizada
# Tabla contiene 3 filas + botones "Ver detalles"
```

---

### Estado 4: Después de Ver Detalle

**Después de clic en "Ver detalles" y cargar detalle**

```python
aspirantes_manager.frame_listado: OCULTO (pack_forget)
aspirantes_manager.frame_detalle: VISIBLE

aspirantes_manager.detalle_actual: {
    'aspirante': {
        'id_aspirante': 2,
        'nombre_completo': 'María García',
        'tipo_identificacion': 'TI',
        'numero_identificacion': '123456789',
        'grado_solicitado': 'Segundo',
        'fecha_solicitud': '28/11/2025',
        'estado_proceso': 'aceptado',
        ...
    },
    'acudiente': {
        'nombre_completo': 'Pedro García',
        'parentesco': 'Padre',
        'email': 'pedro@email.com',
        ...
    },
    'acciones_disponibles': [...]
}

# Vista de detalle renderizada con todas las secciones
```

---

### Estado 5: Después de Volver al Listado

**Después de clic en "← Volver al listado"**

```python
aspirantes_manager.frame_detalle: OCULTO (pack_forget)
aspirantes_manager.frame_listado: VISIBLE

# Tabla sigue con los mismos datos
aspirantes_manager.aspirantes_actuales: [mismos 3 aspirantes]
```

---

## Cómo Visualizar

### Opción 1: PlantUML Online

1. Abrir: https://www.plantuml.com/plantuml/uml/
2. Copiar contenido de `DiagramaSecuencia_Consulta_Aspirantes_UML.puml`
3. Pegar en el editor
4. Presionar Submit o Ctrl+Enter

### Opción 2: VS Code

1. Instalar extensión: **PlantUML** (jebbs.plantuml)
2. Abrir `DiagramaSecuencia_Consulta_Aspirantes_UML.puml`
3. Presionar `Alt+D` (Windows) o `Option+D` (Mac)

### Opción 3: Generar PNG

```bash
# Con Java
java -jar plantuml.jar DiagramaSecuencia_Consulta_Aspirantes_UML.puml

# Con Node.js
npm install -g node-plantuml
puml generate DiagramaSecuencia_Consulta_Aspirantes_UML.puml -o aspirantes.png
```

---

## Referencias

### Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `test_consultar_aspirantes.py` | Tests del caso de uso CU-12 |
| `app/services/servicio_aspirante.py` | Servicio de lógica de negocio (413 líneas) |
| `app/ui/modules/aspirantes.py` | Vista de UI para gestión (769 líneas) |
| `app/ui/modules/director.py` | Dashboard del directivo con botón |
| `app/ui/main.py` | Controlador principal con show_frame() |
| `app/core/usuarios/aspirante.py` | Modelo de dominio Aspirante |
| `app/core/usuarios/acudiente.py` | Modelo de dominio Acudiente |

### Documentos Relacionados

| Documento | Descripción |
|-----------|-------------|
| `DiagramaSecuencia_Consulta_Aspirantes_UML.puml` | Código PlantUML del diagrama |
| `DiagramaSecuencia_Consulta_Aspirantes_Explicado.md` | Este documento |
| `DiagramaSecuencia_Inicio_Aplicacion_UML.puml` | Diagrama de inicialización del sistema |
| `diagInteracccion.pdf` | Documento de referencia UML 2.5 |

### Elementos UML 2.5

| Elemento | Página PDF | Uso en Diagrama |
|----------|------------|-----------------|
| Actores | Pág. 11 | Directivo |
| Líneas de vida | Pág. 6 | 21 participantes |
| Mensajes síncronos | Pág. 10-11 | 115+ mensajes |
| Fragmento `opt` | Pág. 16 | 4 usos condicionales |
| Fragmento `loop` | Pág. 20 | 3 iteraciones |
| Activaciones | Pág. 11 | 80+ focos de control |
| Notas | Pág. 11 | 30+ explicaciones |

---

## Métricas del Diagrama

| Métrica | Valor |
|---------|-------|
| **Participantes** | 21 |
| **Mensajes totales** | 115+ |
| **Fases** | 10 |
| **Consultas a BD** | 3 (2 obligatorias, 1 condicional) |
| **Fragmentos `opt`** | 4 |
| **Fragmentos `loop`** | 3 |
| **Activaciones** | 80+ |
| **Notas explicativas** | 30+ |
| **Puntos de espera** | 2 (listado y detalle) |
| **Líneas de código representadas** | ~500 |
| **Tiempo de ejecución estimado** | 200-500ms (sin red) |

---

## Resumen Ejecutivo

### ¿Qué Representa?

Este diagrama modela **el caso de uso CU-12: Consultar y Gestionar Aspirantes**, mostrando:
- Cómo el directivo accede al módulo de aspirantes
- Cómo el sistema carga y muestra el listado
- Cómo se consulta la base de datos
- Cómo se renderiza la tabla con scrollbar
- Cómo el directivo ve detalles individuales
- Cómo el sistema obtiene información completa del aspirante y acudiente

### ¿Por Qué es Importante?

- ✅ **Documentación del CU-12**: Muestra implementación real del caso de uso
- ✅ **Carga dinámica**: Demuestra lazy loading de módulos para performance
- ✅ **Consultas optimizadas**: Queries con JOINs eficientes
- ✅ **UI responsiva**: Canvas scrollable para tablas grandes
- ✅ **Arquitectura en capas**: Separación clara entre UI, control, lógica y datos

### ¿Para Quién?

- **Desarrolladores**: Para entender la arquitectura del CU-12
- **QA/Testers**: Para diseñar casos de prueba completos
- **Arquitectos**: Para evaluar diseño y performance
- **Documentadores**: Para crear manuales de usuario

---

**Fin del Documento**

*Versión 1.0 - Notación UML 2.5*  
*CU-12: Consultar y Gestionar Aspirantes*  
*Fecha: 12 de Diciembre 2025*
