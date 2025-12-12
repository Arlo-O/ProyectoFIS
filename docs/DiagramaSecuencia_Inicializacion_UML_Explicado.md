# Diagrama de Secuencia UML: Inicialización del Sistema de Gestión Académica

**Versión**: 2.0 - Notación UML 2.5  
**Fecha**: 12 de Diciembre 2025  
**Basado en**: OMG Unified Modeling Language™ (OMG UML) Version 2.5

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Elementos UML Utilizados](#elementos-uml-utilizados)
3. [Descripción del Diagrama](#descripción-del-diagrama)
4. [Fases de Inicialización](#fases-de-inicialización)
5. [Trazas de Ocurrencias](#trazas-de-ocurrencias)
6. [Mensajes y Activaciones](#mensajes-y-activaciones)
7. [Fragmentos Combinados](#fragmentos-combinados)
8. [Líneas de Vida](#líneas-de-vida)
9. [Cómo Visualizar el Diagrama](#cómo-visualizar-el-diagrama)
10. [Referencias](#referencias)

---

## Introducción

### Propósito del Diagrama

Este diagrama de secuencia modela **la interacción completa del proceso de inicialización** del Sistema de Gestión Académica, desde que el usuario ejecuta el script principal hasta que la aplicación queda esperando la interacción del usuario en la pantalla de login.

### Alcance

El diagrama captura:
- ✅ Todas las llamadas a funciones y métodos en orden cronológico
- ✅ Creación y configuración de objetos (ventanas, frames, widgets)
- ✅ Inicialización de servicios y mapeos ORM
- ✅ Configuración de estilos y layouts
- ✅ Estado final del sistema en espera

### Intencionalidad

Según el documento de referencia UML 2.5, este diagrama se utiliza para:

> "Obtener una mejor comprensión de una situación de interacción de entidades estructurales por parte de un diseñador o un equipo de diseño."

En nuestro caso:
- **Comprensión arquitectónica**: Entender cómo se inicializa el sistema completo
- **Documentación**: Referencia para nuevos desarrolladores
- **Debugging**: Identificar dónde ocurren problemas durante el inicio
- **Diseño de pruebas**: Corroborar trazas de ocurrencias esperadas

---

## Elementos UML Utilizados

### 1. Actor

**Notación**: `actor Usuario as user`

**Descripción**: Representa al usuario externo que inicia la ejecución del sistema.

```
┌─────┐
│     │
│ ◉   │  Usuario
│ │   │
│/ \  │
└─────┘
```

En nuestro diagrama: El **Usuario** ejecuta el comando `python run_app.py`

---

### 2. Participantes (Líneas de Vida)

**Notación**: `participant "<<stereotype>>\nNombre" as alias`

**Descripción**: Representan los elementos del sistema que participan en la interacción. Cada participante tiene una **línea de vida** que muestra su existencia durante la interacción.

**Tipos de participantes en nuestro diagrama**:

| Estereotipo | Ejemplo | Significado |
|-------------|---------|-------------|
| `<<script>>` | run_app.py | Script Python ejecutable |
| `<<module>>` | app.ui.main | Módulo Python |
| `<<window>>` | tk.Tk() | Ventana de Tkinter |
| `<<Frame>>` | main_frame | Widget Frame de Tkinter |
| `<<function>>` | create_login_screen() | Función standalone |
| `<<class>>` | LoginForm | Clase instanciable |

**Ejemplo visual**:

```
┌──────────────────────┐
│  <<script>>          │
│  run_app.py          │
└──────────┬───────────┘
           │
           │  ← Línea de vida
           │
           ▼
```

---

### 3. Mensajes

#### 3.1 Mensaje Síncrono (Llamada de Función)

**Notación**: Flecha sólida `→`

**Descripción**: Representa una llamada síncrona donde el emisor espera la respuesta del receptor antes de continuar.

```
A ────────────────► B : mensaje()
```

**Ejemplos en nuestro diagrama**:
- `runapp -> dotenv: load_dotenv()`
- `uimain -> styles: configure_styles(root_window)`
- `logincol -> loginform: create_widgets(...)`

#### 3.2 Mensaje de Retorno

**Notación**: Flecha discontinua `- - - >`

**Descripción**: Representa el retorno de una llamada de función.

```
A ◄- - - - - - - - - B : resultado
```

**Ejemplos en nuestro diagrama**:
- `dotenv --> runapp: variables cargadas`
- `mappers --> runapp: mapeos configurados`
- `showframe --> uimain: frame visible`

#### 3.3 Mensaje de Creación

**Notación**: Flecha con `**`

**Descripción**: Representa la creación de una nueva instancia.

```
A ────────────────► B ** : new B()
```

**Ejemplos en nuestro diagrama**:
- `runapp -> tkwindow ** : root_window = tk.Tk()`
- `uimain -> mainframe ** : main_frame = tk.Frame(root)`
- `logincol -> loginform ** : login_form = LoginForm(...)`

---

### 4. Activaciones (Focos de Control)

**Notación**: Rectángulo vertical en la línea de vida

**Descripción**: Representa el período durante el cual un objeto está ejecutando una operación.

```
    A           B
    │           │
    │──────────►│
    │           ┌┴┐
    │           │ │ ← Activación
    │           │ │
    │◄──────────│ │
    │           └┬┘
    │           │
```

**En el diagrama**:
- `activate participant` / `deactivate participant`
- Muestra cuándo un componente está "activo" procesando lógica

---

### 5. Fragmentos Combinados

#### 5.1 Fragmento `opt` (Opcional)

**Notación**: `opt condición`

**Descripción**: Ejecuta el contenido solo si la condición es verdadera.

```
┌─ opt [condición] ────────────┐
│                              │
│  A ──────────► B : mensaje() │
│                              │
└──────────────────────────────┘
```

**Ejemplo en nuestro diagrama**:

```plantuml
opt IS_DEVELOPMENT == True
    logincol -> logincolframe: mostrar usuarios de prueba
    note right
      Lista de credenciales de prueba
    end note
end
```

#### 5.2 Fragmento `loop` (Iteración)

**Notación**: `loop condición`

**Descripción**: Ejecuta el contenido repetidamente mientras la condición sea verdadera.

```
┌─ loop [para cada elemento] ──┐
│                              │
│  A ──────────► B : proceso() │
│                              │
└──────────────────────────────┘
```

**Ejemplo en nuestro diagrama**:

```plantuml
loop para cada requisito
    precol -> precolframe: crear Label(requisito)
    note right
      Requisitos:
      ✓ Documento de identidad
      ✓ Información acudientes
      ✓ Historial académico
      ✓ Certificado de nacimiento
    end note
end
```

---

### 6. Notas

**Notación**: `note over`, `note left`, `note right`

**Descripción**: Añade información contextual al diagrama.

**Tipos**:

```plantuml
note over A
  Nota sobre A
end note

note left of A
  Nota a la izquierda
end note

note right of A
  Nota a la derecha
end note

note over A, B
  Nota sobre A y B
end note
```

**Ejemplos en nuestro diagrama**:

```plantuml
note over mappers
  Inicializa mapeos SQLAlchemy ORM:
  • persona_table
  • usuario_table
  • rol_table
  ...
end note
```

---

### 7. Separadores de Fases

**Notación**: `== Título ==`

**Descripción**: Divide el diagrama en secciones lógicas.

```plantuml
== FASE 1: Inicialización ==

== FASE 2: Configuración ==
```

**En nuestro diagrama**:
- `== FASE 1: Inicialización del Punto de Entrada ==`
- `== FASE 2: Configuración de la Ventana Principal ==`
- `== FASE 3: Configuración de Estilos ==`
- etc.

---

### 8. Autonumeración

**Notación**: `autonumber "<b>[00]"`

**Descripción**: Numera automáticamente cada mensaje en el diagrama.

**Resultado**: `[01]`, `[02]`, `[03]`, ...

---

## Descripción del Diagrama

### Participantes Principales

| Participante | Rol | Responsabilidad |
|--------------|-----|-----------------|
| **Usuario** | Actor | Inicia la ejecución del sistema |
| **run_app.py** | Script principal | Punto de entrada, orquesta la inicialización |
| **dotenv** | Módulo de configuración | Carga variables de entorno |
| **app.data.mappers** | Módulo ORM | Configura mapeos SQLAlchemy |
| **tk.Tk()** | Ventana Tkinter | Ventana principal de la aplicación |
| **app.ui.main** | Módulo UI | Controlador principal de interfaz |
| **app.ui.styles** | Módulo de estilos | Configura apariencia de componentes |
| **main_frame** | Frame contenedor | Contiene todos los frames de la aplicación |
| **create_nav_commands()** | Función | Crea comandos de navegación |
| **create_login_screen()** | Función | Crea pantalla de login |
| **LoginForm** | Clase | Maneja entrada de credenciales |
| **create_pre_column()** | Función | Crea sección de pre-inscripción |
| **show_frame()** | Función | Controla visibilidad de frames |

---

## Fases de Inicialización

### FASE 1: Inicialización del Punto de Entrada

**Duración**: Mensajes [01] a [11]

**Objetivo**: Cargar configuración y preparar base de datos

**Secuencia**:

1. **Usuario ejecuta el script**
   ```bash
   python run_app.py
   ```

2. **Carga de variables de entorno**
   - `load_dotenv()` lee archivo `.env`
   - Variables disponibles: ENVIRONMENT, credenciales de prueba, configuración BD

3. **Inicialización de mapeos ORM**
   - `start_mappers()` configura SQLAlchemy
   - Mapea 17 tablas a clases Python
   - Establece relaciones entre entidades

4. **Creación de ventana raíz**
   - `tk.Tk()` crea ventana principal
   - Se asigna a `root_window`

**Estado al finalizar**:
- ✅ Variables de entorno cargadas
- ✅ ORM configurado y listo
- ✅ Ventana Tkinter creada

---

### FASE 2: Configuración de la Ventana Principal

**Duración**: Mensajes [12] a [17]

**Objetivo**: Configurar propiedades de la ventana raíz

**Secuencia**:

1. **Asignación a variable global**
   ```python
   root = root_window
   ```

2. **Configuración de propiedades**
   - Título: "Sistema de Gestión Académica"
   - Tamaño: 1400x800 píxeles
   - Grid: Columna y fila expandibles (weight=1)

**Estado al finalizar**:
- ✅ Ventana configurada y lista para recibir contenido

---

### FASE 3: Configuración de Estilos

**Duración**: Mensajes [18] a [25]

**Objetivo**: Aplicar estilos a componentes Tkinter

**Secuencia**:

1. **Crear gestor de estilos**
   ```python
   style = ttk.Style()
   ```

2. **Establecer tema base**
   ```python
   theme_use('clam')
   ```

3. **Configurar estilos de botones**
   - `Admin.TButton`: Azul (#007bff)
   - `Pre.TButton`: Verde (#28a745)
   - `Director.TButton`, `Teacher.TButton`, etc.

**Estado al finalizar**:
- ✅ Todos los estilos definidos
- ✅ Componentes ttk pueden usar estilos personalizados

---

### FASE 4: Creación del Frame Principal

**Duración**: Mensajes [26] a [31]

**Objetivo**: Crear contenedor principal para todos los frames

**Secuencia**:

1. **Crear Frame**
   ```python
   main_frame = tk.Frame(root)
   ```

2. **Posicionar en grid**
   ```python
   main_frame.grid(row=0, column=0, sticky="nsew")
   ```

3. **Configurar expansión**
   - Columna 0: peso 1 (expandible horizontalmente)
   - Fila 0: peso 1 (expandible verticalmente)

**Estado al finalizar**:
- ✅ Frame principal creado y posicionado
- ✅ Listo para recibir sub-frames

---

### FASE 5: Creación de Comandos de Navegación

**Duración**: Mensajes [32] a [33]

**Objetivo**: Crear diccionario de comandos para navegación

**Secuencia**:

1. **Llamar función**
   ```python
   nav_commands = create_nav_commands()
   ```

2. **Crear diccionario**
   ```python
   nav_cmds = {
       'home': lambda: show_frame("login"),
       'logout': logout,
       'dashboard_home': lambda: show_frame("dashboard"),
       # ... más comandos
   }
   ```

**Estado al finalizar**:
- ✅ Diccionario `nav_commands` disponible globalmente
- ✅ 10 comandos de navegación registrados

---

### FASE 6: Creación de Pantalla de Login

**Duración**: Mensajes [34] a [90]

**Objetivo**: Construir la interfaz completa de login

**Secuencia**:

1. **Crear layout principal**
   - Frame con 2 columnas expandibles

2. **Crear columna de autenticación** (Izquierda)
   - Header con título del sistema
   - Subtítulo con nombre del colegio
   - Frame centrado (350x450 píxeles)
   - Título "Autenticación de Usuario"
   - **LoginForm** (campos de usuario y contraseña)
   - Botón "Acceder"
   - Link "¿Olvidó su contraseña?"
   - Usuarios de prueba (solo en desarrollo)

3. **Crear columna de pre-inscripción** (Derecha)
   - Header "Pre-inscripción"
   - Subtítulo "Nuevo estudiante"
   - Pregunta "¿Eres nuevo en nuestra institución?"
   - Texto descriptivo
   - Botón "Iniciar Pre-inscripción"
   - Lista de requisitos (4 items)

4. **Posicionar columnas**
   - Columna izquierda: grid(row=0, column=0)
   - Columna derecha: grid(row=0, column=1)

**Sub-secuencia: Creación de LoginForm**

Mensajes [52] a [66]:

1. **Instanciar clase**
   ```python
   login_form = LoginForm(login_main, {})
   ```

2. **Crear widgets**
   - Label "Usuario:"
   - Entry con placeholder "Ingrese su usuario"
   - Label "Contraseña:"
   - Entry con placeholder "Ingrese su contraseña"

3. **Configurar placeholders**
   - Eventos `<FocusIn>`: borra placeholder
   - Eventos `<FocusOut>`: muestra placeholder si vacío
   - Para contraseña: `show="*"` cuando tiene foco

**Estado al finalizar**:
- ✅ Pantalla de login completamente construida
- ✅ Todos los widgets creados y posicionados
- ✅ Eventos configurados

---

### FASE 7: Mostrar Pantalla de Login

**Duración**: Mensajes [91] a [98]

**Objetivo**: Hacer visible la pantalla de login

**Secuencia**:

1. **Llamar show_frame**
   ```python
   show_frame("login")
   ```

2. **Obtener frame del diccionario**
   ```python
   frame = frames.get("login")
   ```

3. **Ocultar otros frames**
   ```python
   for other_frame in frames.values():
       other_frame.grid_remove()
   ```

4. **Mostrar frame de login**
   ```python
   frame.grid(row=0, column=0, sticky="nsew")
   ```

5. **Actualizar índice**
   ```python
   step_index = -1
   ```

**Estado al finalizar**:
- ✅ Frame de login visible
- ✅ Otros frames ocultos
- ✅ step_index actualizado

---

### FASE 8: Inicio del Event Loop

**Duración**: Mensaje [99]

**Objetivo**: Iniciar bucle de eventos de Tkinter

**Secuencia**:

1. **Llamar mainloop**
   ```python
   root_window.mainloop()
   ```

2. **Bucle infinito**
   - Espera eventos del usuario
   - Procesa clics, teclas, movimientos
   - Redibuja ventana cuando es necesario
   - No retorna hasta cerrar ventana

**Estado final del sistema**:

```
┌──────────────────────────────────────────────────────────┐
│          Sistema de Gestión Académica                     │
├─────────────────────────┬────────────────────────────────┤
│                         │                                │
│  AUTENTICACIÓN          │  PRE-INSCRIPCIÓN               │
│                         │                                │
│  Usuario: [________]    │  ¿Eres nuevo en nuestra        │
│  Contraseña: [_____]    │  institución?                  │
│                         │                                │
│  [    Acceder     ]     │  [Iniciar Pre-inscripción]     │
│                         │                                │
│  ¿Olvidó contraseña?    │  Requisitos:                   │
│                         │  ✓ Documento de identidad      │
│  Usuarios de prueba:    │  ✓ Información acudientes      │
│  • admin@test.com       │  ✓ Historial académico         │
│  • director@test.com    │  ✓ Certificado nacimiento      │
│  • teacher@test.com     │                                │
│  • parent@test.com      │                                │
│                         │                                │
└─────────────────────────┴────────────────────────────────┘

ESPERANDO INTERACCIÓN DEL USUARIO...
```

**Acciones disponibles**:

| Acción | Evento | Handler |
|--------|--------|---------|
| Escribir en campo Usuario | `<KeyPress>` | LoginForm._user_entry |
| Escribir en campo Contraseña | `<KeyPress>` | LoginForm._pass_entry |
| Clic en "Acceder" | `<Button-1>` | `login_to_dashboard()` |
| Clic en "¿Olvidó contraseña?" | `<Button-1>` | `abrir_recuperar_password()` |
| Clic en "Iniciar Pre-inscripción" | `<Button-1>` | `start_preinscription()` |
| Cerrar ventana | `WM_DELETE_WINDOW` | `exit` |

---

## Trazas de Ocurrencias

### Definición (según UML 2.5)

> "La semántica de una interacción se establece por medio de dos conjuntos de trazas (Secuencia de ocurrencias de eventos): **Válidas** e **inválidas**."

### Traza Válida Principal

Secuencia correcta de inicialización:

```
1. Usuario ejecuta script
2. run_app.py carga dotenv
3. run_app.py inicializa mappers
4. run_app.py crea tk.Tk()
5. run_app.py llama initialize_app()
6. initialize_app() configura ventana
7. initialize_app() aplica estilos
8. initialize_app() crea main_frame
9. initialize_app() crea nav_commands
10. initialize_app() crea login_screen
    10.1. create_login_screen() crea layout
    10.2. create_login_column() crea columna izquierda
        10.2.1. LoginForm crea widgets
    10.3. create_pre_column() crea columna derecha
11. initialize_app() llama show_frame("login")
12. run_app.py llama mainloop()
13. Sistema espera eventos
```

### Trazas Inválidas

**Traza inválida 1: Crear ventana antes de cargar dotenv**
```
❌ 1. Usuario ejecuta script
❌ 2. run_app.py crea tk.Tk()
❌ 3. run_app.py carga dotenv  ← ERROR: Variables no disponibles
```

**Traza inválida 2: Llamar show_frame antes de crear frame**
```
❌ 1. initialize_app() llama show_frame("login")
❌ 2. show_frame() busca frames["login"]  ← ERROR: Frame no existe
```

**Traza inválida 3: Crear LoginForm antes de crear parent**
```
❌ 1. login_form = LoginForm(login_main, {})
❌ 2. login_main no existe  ← ERROR: Parent no creado
```

### Invariantes de Estado

Estados que deben cumplirse en puntos específicos:

| Punto | Invariante |
|-------|-----------|
| Antes de initialize_app() | `root_window != None` |
| Antes de create_login_screen() | `main_frame != None` |
| Antes de show_frame() | `"login" in frames` |
| Antes de mainloop() | `root.winfo_exists() == True` |
| Después de initialize_app() | `len(nav_commands) == 10` |

---

## Mensajes y Activaciones

### Tabla Completa de Mensajes

| # | Emisor | Receptor | Mensaje | Tipo | Retorno |
|---|--------|----------|---------|------|---------|
| 01 | Usuario | run_app.py | ejecuta python run_app.py | Síncrono | - |
| 02 | run_app.py | dotenv | load_dotenv() | Síncrono | variables cargadas |
| 03 | run_app.py | mappers | start_mappers() | Síncrono | mapeos configurados |
| 04 | mappers | mappers | mapper_registry.configure() | Auto-delegación | - |
| 05 | run_app.py | tk.Tk | root_window = tk.Tk() | Creación | instancia |
| 06 | run_app.py | ui.main | initialize_app(root_window) | Síncrono | - |
| 07 | ui.main | ui.main | root = root_window | Asignación | - |
| 08 | ui.main | tk.Tk | title("Sistema...") | Síncrono | - |
| 09 | ui.main | tk.Tk | geometry("1400x800") | Síncrono | - |
| 10 | ui.main | tk.Tk | grid_columnconfigure(0, weight=1) | Síncrono | - |
| 11 | ui.main | tk.Tk | grid_rowconfigure(0, weight=1) | Síncrono | - |
| 12 | ui.main | styles | configure_styles(root_window) | Síncrono | estilos aplicados |
| ... | ... | ... | ... | ... | ... |

*(Tabla completa con 99+ mensajes disponible en el diagrama .puml)*

### Tipos de Activación

**1. Activación Simple**
```
A ──────────► B
              ┌┴┐
              │ │ ← Procesa
              └┬┘
A ◄──────────  B
```

**2. Activación Anidada**
```
A ──────────► B
              ┌┴┐
              │ │──────────► C
              │ │            ┌┴┐
              │ │            │ │ ← Procesa
              │ │◄────────── │ │
              │ │            └┬┘
              └┬┘
A ◄──────────  B
```

**3. Auto-delegación**
```
    A
    │
    │──┐
    │  │ mensaje_a_sí_mismo()
    │◄─┘
    │
```

**Ejemplo en el diagrama**:
```plantuml
mappers -> mappers: mapper_registry.configure()
activate mappers
deactivate mappers
```

---

## Fragmentos Combinados

### Fragmentos Utilizados en el Diagrama

#### 1. Fragmento `opt` (Opcional)

**Ubicación**: Creación de columna de autenticación, mensaje ~[70]

**Código**:
```plantuml
opt IS_DEVELOPMENT == True
    logincol -> logincolframe: mostrar usuarios de prueba
    activate logincolframe
    note right
      Lista de credenciales de prueba:
      • admin@test.com / admin123 (Admin)
      • director@test.com / director123 (Director)
      • teacher@test.com / teacher123 (Profesor)
      • parent@test.com / parent123 (Acudiente)
    end note
    deactivate logincolframe
end
```

**Semántica**:
- **Condición**: Variable de entorno `IS_DEVELOPMENT == True`
- **Operando**: Mostrar lista de usuarios de prueba en la UI
- **Comportamiento**: 
  - Si `IS_DEVELOPMENT == True`: Se muestran los usuarios de prueba
  - Si `IS_DEVELOPMENT == False`: No se muestra nada

**Justificación**:
En modo producción, no debe mostrarse información sensible de usuarios de prueba.

---

#### 2. Fragmento `loop` (Iteración)

**Ubicación**: Creación de columna de pre-inscripción, mensajes ~[84-87]

**Código**:
```plantuml
loop para cada requisito
    precol -> precolframe: crear Label(requisito)
    activate precolframe
    note right
      Requisitos:
      ✓ Documento de identidad
      ✓ Información acudientes
      ✓ Historial académico
      ✓ Certificado de nacimiento
    end note
    deactivate precolframe
end
```

**Semántica**:
- **Condición**: Para cada elemento en lista `requisitos`
- **Operando**: Crear un Label con el texto del requisito
- **Comportamiento**: 
  - Itera sobre la lista: `["✓ Documento...", "✓ Información...", ...]`
  - Por cada string, crea un widget Label
  - Lo posiciona en el frame

**Código Python equivalente**:
```python
requisitos = [
    "✓ Documento de identidad del estudiante",
    "✓ Información de los acudientes",
    "✓ Historial académico anterior",
    "✓ Certificado de nacimiento"
]
for req in requisitos:
    tk.Label(pre_main_container, text=req, 
             bg=COLOR_ACCENT_DARK, fg="#e0e0e0", 
             font=FONT_SMALL).pack(anchor="w", pady=2)
```

---

#### 3. Fragmento `loop` (Ocultar frames)

**Ubicación**: Función show_frame(), mensajes ~[93-95]

**Código**:
```plantuml
loop para cada frame en frames.values()
    showframe -> mainframe: other_frame.grid_remove()
    activate mainframe
    note right
      Oculta todos los frames
      (sin destruirlos)
    end note
    deactivate mainframe
end
```

**Semántica**:
- **Condición**: Para cada frame en diccionario `frames`
- **Operando**: Llamar `grid_remove()` en el frame
- **Comportamiento**: 
  - Itera sobre todos los frames registrados
  - Oculta cada frame (sin destruirlo)
  - Permite que solo un frame sea visible a la vez

**Código Python equivalente**:
```python
for other_frame in frames.values():
    if other_frame and isinstance(other_frame, tk.Widget):
        other_frame.grid_remove()
```

---

### Otros Fragmentos Combinados Disponibles en UML 2.5

Aunque no se usan en este diagrama, el documento de referencia menciona:

| Fragmento | Descripción | Uso potencial |
|-----------|-------------|---------------|
| `alt` | Alternativa | Seleccionar entre login o recuperar contraseña |
| `break` | Romper ejecución | Abortar inicialización si falla dotenv |
| `par` | Paralelo | Cargar múltiples módulos simultáneamente |
| `seq` | Secuencial débil | Operaciones sin orden estricto |
| `strict` | Secuencial estricto | Operaciones que deben ser ordenadas |
| `neg` | Trazas inválidas | Documentar secuencias incorrectas |
| `critical` | Región atómica | Operaciones que no deben interrumpirse |
| `ignore` | Ignorar mensajes | Mensajes no relevantes para esta vista |
| `consider` | Considerar mensajes | Filtrar solo mensajes específicos |
| `assert` | Aserción | Verificar estado del sistema |

---

## Líneas de Vida

### Definición

> "Una línea de vida representa un participante individual en la interacción. Su sintaxis gráfica es un rectángulo con una línea vertical discontinua."

### Sintaxis Abstracta (según documento UML 2.5)

```
┌──────────────────────┐
│  Participante        │
│  :Clase              │
└──────────┬───────────┘
           │
           │  ← Línea de vida
           │
           ▼
```

### Líneas de Vida en Nuestro Diagrama

| Línea de Vida | Clase/Tipo | Creación | Destrucción | Duración |
|---------------|------------|----------|-------------|----------|
| Usuario | Actor | Antes del diagrama | Después del diagrama | Todo el diagrama |
| run_app.py | Script | Mensaje [01] | Después de mainloop() | Todo el diagrama |
| dotenv | Módulo | Antes del diagrama | - | Cargado en memoria |
| mappers | Módulo | Antes del diagrama | - | Cargado en memoria |
| tkwindow | tk.Tk | Mensaje [05] | Al cerrar ventana | Desde creación |
| uimain | Módulo | Antes del diagrama | - | Cargado en memoria |
| styles | Módulo | Antes del diagrama | - | Cargado en memoria |
| main_frame | tk.Frame | Mensaje [26] | Al cerrar ventana | Desde creación |
| navcommands | Function | Mensajes [32-33] | - | Ejecución breve |
| loginscreen | Function | Mensajes [34-90] | - | Ejecución breve |
| loginlayout | tk.Frame | Mensaje [36] | Al cerrar ventana | Desde creación |
| logincol | Function | Mensajes [42-72] | - | Ejecución breve |
| logincolframe | tk.Frame | Mensaje [43] | Al cerrar ventana | Desde creación |
| loginform | LoginForm | Mensaje [52] | Al cerrar ventana | Desde creación |
| precol | Function | Mensajes [73-88] | - | Ejecución breve |
| precolframe | tk.Frame | Mensaje [74] | Al cerrar ventana | Desde creación |
| showframe | Function | Mensajes [91-98] | - | Ejecución breve |

### Tipos de Líneas de Vida

**1. Persistentes** (existen durante todo el diagrama):
- Usuario
- run_app.py
- Módulos cargados (dotenv, mappers, uimain, styles)

**2. Creadas durante la interacción**:
- tkwindow (tk.Tk)
- main_frame
- loginlayout
- logincolframe
- loginform
- precolframe

**3. Temporales** (funciones que ejecutan y retornan):
- navcommands
- loginscreen
- logincol
- precol
- showframe

---

## Cómo Visualizar el Diagrama

### Opción 1: PlantUML Online

1. Ir a: https://www.plantuml.com/plantuml/uml/
2. Abrir archivo: `DiagramaSecuencia_Inicio_Aplicacion_UML.puml`
3. Copiar todo el contenido
4. Pegarlo en el editor online
5. Click en "Submit" o presionar Ctrl+Enter
6. El diagrama se renderizará automáticamente

### Opción 2: VS Code con extensión

1. Instalar extensión: **PlantUML** (por jebbs)
2. Abrir archivo: `DiagramaSecuencia_Inicio_Aplicacion_UML.puml`
3. Presionar: `Alt+D` (Windows/Linux) o `Option+D` (Mac)
4. El diagrama se mostrará en vista previa

### Opción 3: Generar imagen PNG/SVG

**Instalar PlantUML**:
```bash
# Opción 1: Usando Java
java -jar plantuml.jar DiagramaSecuencia_Inicio_Aplicacion_UML.puml

# Opción 2: Usando Node.js
npm install -g node-plantuml
puml generate DiagramaSecuencia_Inicio_Aplicacion_UML.puml -o output.png
```

**Resultado**: Archivo de imagen con el diagrama renderizado

### Opción 4: Integración con documentación

**Markdown con PlantUML**:
```markdown
# Mi Documentación

## Diagrama de Secuencia

![Diagrama](DiagramaSecuencia_Inicio_Aplicacion_UML.puml)
```

**Compatible con**:
- GitLab (soporte nativo)
- GitHub (con extensiones)
- Confluence (con plugins)
- Sphinx (con sphinxcontrib-plantuml)

---

## Referencias

### Documentos Base

1. **OMG Unified Modeling Language™ (OMG UML) Version 2.5**
   - Organización: Object Management Group
   - Año: 2015
   - URL: https://www.omg.org/spec/UML/2.5/

2. **Diagramas de Interacción** (Documento PDF adjunto)
   - Autor: HAD
   - Contenido: Notación y semántica de diagramas de interacción UML
   - Páginas: 32 diapositivas

### Elementos UML Cubiertos

| Elemento | Sección PDF | Descripción |
|----------|-------------|-------------|
| Definición general | Pág. 2 | Concepto de interacciones |
| Intencionalidad | Pág. 3 | Para qué se usan |
| Variantes de diagramas | Pág. 4 | Tipos de diagramas de interacción |
| Sintaxis abstracta | Págs. 5-9 | Metamodelo UML |
| Diagramas de secuencia | Pág. 11 | Notación básica |
| Tipos de mensajes | Pág. 10 | Mensajes síncronos, asíncronos, creación |
| Fragmentos combinados | Págs. 15-21 | alt, opt, loop, par, etc. |
| Líneas de vida | Pág. 6 | Sintaxis abstracta |
| Activaciones | Pág. 11 | Focos de control |

### Herramientas Recomendadas

| Herramienta | Tipo | URL |
|-------------|------|-----|
| PlantUML | Generador de diagramas | https://plantuml.com/ |
| VS Code + PlantUML | Editor + extensión | https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml |
| draw.io | Editor visual | https://app.diagrams.net/ |
| Lucidchart | Editor comercial | https://www.lucidchart.com/ |
| Enterprise Architect | Herramienta CASE | https://sparxsystems.com/ |

### Archivos Relacionados

| Archivo | Descripción |
|---------|-------------|
| `DiagramaSecuencia_Inicio_Aplicacion_UML.puml` | Código PlantUML del diagrama |
| `Diagrama_Secuencia_Inicializacion.md` | Documentación anterior (formato simple) |
| `DiagramaSecuencia_Inicializacion_UML_Explicado.md` | Este documento (formato UML 2.5) |
| `run_app.py` | Código fuente del punto de entrada |
| `app/ui/main.py` | Código fuente del módulo UI principal |
| `app/ui/components/login.py` | Código fuente de LoginForm |

---

## Resumen Ejecutivo

### ¿Qué representa este diagrama?

Este diagrama de secuencia UML 2.5 modela la **inicialización completa del Sistema de Gestión Académica**, desde la ejecución del script principal hasta que la ventana de login queda esperando la interacción del usuario.

### ¿Por qué usar notación UML 2.5?

La notación UML 2.5 es el **estándar internacional para modelado de software**:
- ✅ **Lenguaje universal**: Entendido por desarrolladores en todo el mundo
- ✅ **Semántica formal**: Significado preciso y sin ambigüedades
- ✅ **Herramientas compatibles**: Soporte en múltiples herramientas CASE
- ✅ **Documentación profesional**: Cumple estándares de ingeniería de software

### ¿Qué aprendemos del diagrama?

1. **Orden de inicialización**: Secuencia exacta de operaciones
2. **Dependencias**: Qué componentes dependen de otros
3. **Flujo de control**: Cómo se pasa el control entre componentes
4. **Creación de objetos**: Cuándo y cómo se instancian objetos
5. **Configuración**: Cómo se configuran ventana, estilos, frames

### ¿Para quién es este diagrama?

- **Desarrolladores nuevos**: Para entender la arquitectura
- **Desarrolladores experimentados**: Para debugging y refactoring
- **Arquitectos de software**: Para evaluar el diseño
- **QA/Testers**: Para diseñar casos de prueba
- **Documentadores técnicos**: Para crear manuales

### Métricas del Diagrama

| Métrica | Valor |
|---------|-------|
| **Participantes** | 15 |
| **Mensajes** | 99+ |
| **Fases** | 8 |
| **Fragmentos combinados** | 3 (1 opt, 2 loop) |
| **Activaciones** | 60+ |
| **Líneas de código representadas** | ~200 |
| **Duración de ejecución real** | ~500ms |

---

**Fin del documento**

*Versión 2.0 - Notación UML 2.5*  
*Fecha: 12 de Diciembre 2025*  
*Autor: Sistema de Gestión Académica - Equipo de Desarrollo*
