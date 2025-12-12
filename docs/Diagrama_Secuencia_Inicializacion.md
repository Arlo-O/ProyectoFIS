# Diagrama de Secuencia: Inicialización de la Aplicación

**Fecha**: 12 de Diciembre 2025  
**Versión**: 1.0  
**Última Actualización**: Sistema en operación

---

## 📋 Índice de Contenidos

1. [Listado de Clases Involucradas](#listado-de-clases-involucradas)
2. [Diagrama de Secuencia Detallado](#diagrama-de-secuencia-detallado)
3. [Flujo Visual ASCII](#flujo-visual-ascii)
4. [Estados Finales](#estados-finales)

---

## Listado de Clases Involucradas

### Orden de Participación (desde inicio hasta pantalla de espera)

| # | Módulo | Clase/Función | Rol | Descripción |
|---|--------|---------------|-----|------------|
| 1 | `run_app.py` | Función principal `if __name__ == "__main__"` | Punto de entrada | Inicia el programa Python |
| 2 | `run_app.py` | Sistema de importes | Gestor de módulos | Carga variables de entorno y módulos necesarios |
| 3 | `app.data.mappers` | `start_mappers()` | Inicializador ORM | Configura mapeos SQLAlchemy |
| 4 | `app.ui.main` | `initialize_app(root_window)` | Inicializador de UI | Punto de entrada de interfaz gráfica |
| 5 | `app.ui.styles` | `configure_styles(root_window)` | Configurador de estilos | Aplica estilos a componentes Tkinter |
| 6 | `app.ui.main` | `create_nav_commands()` | Creador de comandos | Construye diccionario de navegación |
| 7 | `app.ui.main` | `create_login_screen(parent_frame)` | Creador de pantalla | Crea pantalla de login |
| 8 | `app.ui.main` | `create_login_column(parent, login_command)` | Creador de columna | Crea sección de autenticación |
| 9 | `app.ui.components.login` | `LoginForm` | Formulario de entrada | Clase para manejo de credenciales |
| 10 | `app.ui.main` | `create_pre_column(parent)` | Creador de columna | Crea sección de pre-inscripción |
| 11 | `tkinter` | `tk.Tk()` | Ventana principal | Ventana raíz de la aplicación |
| 12 | `tkinter.ttk` | Componentes estilos | Widgets estilizados | Botones, etiquetas, campos |

### Clases de Servicios (Cargadas pero no usadas hasta login)

| Módulo | Clase | Rol | Momento de Uso |
|--------|-------|-----|----------------| 
| `app.services.auth_service` | `AuthenticationService` | Autenticación | Después del login |
| `app.services.rbac_service` | `rbac_service` | Control de acceso | Después del login |
| `app.config.database` | `SessionLocal` | Sesión de BD | Cuando se necesite consultar |

---

## Diagrama de Secuencia Detallado

### FASE 1: INICIALIZACIÓN DE PUNTO DE ENTRADA

#### **PASO 1: Ejecución del Script Principal**

**Archivo**: `run_app.py` (líneas 1-31)  
**Clase**: Módulo principal Python  
**Evento**: Usuario ejecuta `python run_app.py` o similar

```python
# run_app.py, línea 27-30
if __name__ == "__main__":
    root_window = tk.Tk()
    try:
        initialize_app(root_window)
        root_window.mainloop()
```

**Acciones**:
- Crea instancia de `tk.Tk()` → ventana raíz de Tkinter
- Asigna a variable global `root_window`
- Llama a `initialize_app(root_window)`

**Siguiente**: PASO 2

---

#### **PASO 2: Carga de Variables de Entorno**

**Archivo**: `run_app.py` (línea 15)  
**Clase**: `dotenv.load_dotenv()`  
**Evento**: Se ejecuta como parte del módulo `run_app.py`

```python
# run_app.py, línea 15
from dotenv import load_dotenv
load_dotenv()
```

**Acciones**:
- Lee archivo `.env` en el directorio raíz
- Carga variables de entorno del proyecto:
  - `ENVIRONMENT`: modo "development" o "production"
  - `TEST_ADMIN_EMAIL`, `TEST_ADMIN_PASSWORD`
  - `TEST_DIRECTOR_EMAIL`, `TEST_DIRECTOR_PASSWORD`
  - `TEST_TEACHER_EMAIL`, `TEST_TEACHER_PASSWORD`
  - `TEST_PARENT_EMAIL`, `TEST_PARENT_PASSWORD`
  - Variables de conexión a BD
  - Otras configuraciones

**Siguiente**: PASO 3

---

#### **PASO 3: Inicialización de Mapeos ORM (SQLAlchemy)**

**Archivo**: `run_app.py` (línea 18-21)  
**Clase**: `app.data.mappers.start_mappers()`  
**Evento**: Antes de importar módulos que usen modelos ORM

```python
# run_app.py, línea 18-21
try:
    from app.data.mappers import start_mappers
    start_mappers()
except Exception as e:
    print(f"Warning: no se pudieron inicializar los mapeos: {e}")
```

**Acciones dentro de `start_mappers()`**:
1. Importa `mapper_registry` (instancia global de SQLAlchemy)
2. Define tabla `persona_table` → Table('persona', metadata, ...)
3. Define tabla `usuario_table` → Table('usuario', metadata, ...)
4. Define tabla `rol_table` → Table('rol', metadata, ...)
5. Define tabla `permiso_table` → Table('permiso', metadata, ...)
6. Define tabla `aspirante_table` → Table('aspirante', metadata, ...)
7. Define tabla `estudiante_table` → Table('estudiante', metadata, ...)
8. Define tabla `profesor_table` → Table('profesor', metadata, ...)
9. Define tabla `director_table` → Table('director', metadata, ...)
10. Define tabla `acudiente_table` → Table('acudiente', metadata, ...)
11. Define tabla `grupo_table` → Table('grupo', metadata, ...)
12. Define tabla `curso_table` → Table('curso', metadata, ...)
13. Define tabla `evaluacion_table` → Table('evaluacion', metadata, ...)
14. Define tabla `logro_table` → Table('logro', metadata, ...)
15. Define tabla `observador_table` → Table('observador', metadata, ...)
16. Define tabla `anotacion_table` → Table('anotacion', metadata, ...)
17. Define tabla `hoja_vida_table` → Table('hoja_vida', metadata, ...)
18. Llama `mapper_registry.configure()` → establece relaciones entre clases

**Estado después**: ORM listo, modelos mapeados a tablas

**Siguiente**: PASO 4

---

### FASE 2: INICIALIZACIÓN DE INTERFAZ GRÁFICA

#### **PASO 4: Llamada a `initialize_app(root_window)`**

**Archivo**: `app/ui/main.py` (línea 665-716)  
**Clase**: Función `initialize_app(root_window)`  
**Evento**: `run_app.py` línea 29 llama esta función

```python
# app/ui/main.py, línea 665-672
def initialize_app(root_window):
    global root, frames, nav_commands, main_frame
    
    root = root_window
    root.title("Sistema de Gestión Académica")
    root.geometry("1400x800")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
```

**Acciones**:
1. Asigna `root_window` a variable global `root`
2. Establece título de ventana: `"Sistema de Gestión Académica"`
3. Establece tamaño: `1400x800` píxeles
4. Configura grid: columna 0 con peso 1 (expandible)
5. Configura grid: fila 0 con peso 1 (expandible)

**Estado de variables globales**:
- `root`: Referencia a ventana Tk
- `frames`: {} (dict vacío)
- `nav_commands`: {} (dict vacío)
- `main_frame`: None (aún no creado)

**Siguiente**: PASO 5

---

#### **PASO 5: Importación de Módulos de Estilos y Componentes**

**Archivo**: `app/ui/main.py` (línea 13-30)  
**Clase**: Importaciones del módulo  
**Evento**: Cuando Python carga `app/ui/main.py`

```python
# app/ui/main.py, línea 13-30
from .config import *  # Constantes de colores y fuentes
from .styles import configure_styles  # Función para estilos
from .components.session import set_current_role, set_user_info, clear_session
from .components.login import LoginForm
from .components.recuperar_password import RecuperarPasswordWindow
from app.services.auth_service import AuthenticationService
from app.services.rbac_service import rbac_service
from .components.form import create_step1, create_step2, create_step3, create_step4
```

**Módulos cargados**:

1. **`app/ui/config.py`**: Constantes de UI
   - `COLOR_BG_LOGIN`, `COLOR_DARK_BG`, `COLOR_HEADER_PRE`
   - `FONT_H1`, `FONT_H2`, `FONT_P`, `FONT_SMALL`
   - `COLOR_ACCENT_DARK`, `COLOR_TEXT_PLACEHOLDER`

2. **`app/ui/styles.py`**: Configuración de estilos Tkinter
   - Función `configure_styles(root_window)`
   - Define estilos para `Admin.TButton`, `Pre.TButton`, etc.

3. **`app/ui/components/login.py`**: Clase LoginForm
   - Maneja entrada de credenciales
   - Implementa placeholders

4. **`app/services/auth_service.py`**: AuthenticationService
   - Instanciada en variable global `auth_service`
   - No usada hasta login

5. **`app/services/rbac_service.py`**: Control de acceso basado en roles
   - Instanciada en variable global `rbac_service`
   - No usada hasta login

**Estado después**: Todos los módulos necesarios cargados en memoria

**Siguiente**: PASO 6

---

#### **PASO 6: Configuración de Estilos Tkinter**

**Archivo**: `app/ui/main.py` (línea 674)  
**Función**: `configure_styles(root_window)`  
**Evento**: Llamada dentro de `initialize_app()`

```python
# app/ui/main.py, línea 674
configure_styles(root_window)
```

**Lo que hace `configure_styles()` en `app/ui/styles.py`**:

```python
# app/ui/styles.py
def configure_styles(root):
    style = ttk.Style()
    
    # Tema base
    style.theme_use('clam')
    
    # Estilo Admin.TButton
    style.configure('Admin.TButton',
                   background='#007bff',
                   foreground='white',
                   font=('Segoe UI', 10, 'bold'),
                   padding=10)
    
    # Estilo Pre.TButton
    style.configure('Pre.TButton',
                   background='#28a745',
                   foreground='white',
                   font=('Segoe UI', 10, 'bold'),
                   padding=10)
    
    # Más estilos para otros botones...
```

**Acciones**:
1. Obtiene instancia de `ttk.Style()` (gestor de estilos)
2. Establece tema: `'clam'`
3. Configura estilo `Admin.TButton` con color azul, fuente, padding
4. Configura estilo `Pre.TButton` con color verde
5. Configura estilos adicionales para otros componentes
6. Aplica los estilos a la ventana raíz

**Estado después**: Todos los estilos Tkinter definidos y aplicados

**Siguiente**: PASO 7

---

#### **PASO 7: Creación del Frame Principal**

**Archivo**: `app/ui/main.py` (línea 675-680)  
**Clase**: `tk.Frame`  
**Evento**: Dentro de `initialize_app()`

```python
# app/ui/main.py, línea 675-680
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
```

**Acciones**:
1. Crea frame contenedor: `tk.Frame(root)`
2. Lo posiciona en grid: `grid(row=0, column=0, sticky="nsew")`
   - `sticky="nsew"`: Estira en todas las direcciones (norte, sur, este, oeste)
3. Configura columna 0 con peso 1: contenido expandible horizontalmente
4. Configura fila 0 con peso 1: contenido expandible verticalmente

**Estado global**: Variable global `main_frame` ahora contiene referencia a Frame

**Siguiente**: PASO 8

---

#### **PASO 8: Creación de Diccionario de Comandos de Navegación**

**Archivo**: `app/ui/main.py` (línea 682-683)  
**Función**: `create_nav_commands()`  
**Evento**: Dentro de `initialize_app()`

```python
# app/ui/main.py, línea 682-683
nav_commands = create_nav_commands()
print("DEBUG: nav_commands creado")
```

**Lo que hace `create_nav_commands()` en línea 633-647**:

```python
def create_nav_commands():
    """Crea el diccionario de comandos de navegación"""
    nav_cmds = {
        'home': lambda: show_frame("login"),
        'logout': logout,
        'dashboard_home': lambda: show_frame("dashboard"),
        'director_home': lambda: show_frame("director_dashboard"),
        'teacher_home': lambda: show_frame("teacher_dashboard"),
        'parent_home': lambda: show_frame("parent_dashboard"),
        'show_frame': show_frame,
        'next': lambda: next_step(),
        'prev': lambda: prev_step(),
        'submit': lambda: submit_form(),
    }
    return nav_cmds
```

**Acciones**:
1. Crea diccionario vacío `nav_cmds = {}`
2. Agrega 10 comandos (funciones lambda y referencias):
   - `'home'`: función lambda que llama `show_frame("login")`
   - `'logout'`: referencia a función `logout`
   - `'dashboard_home'`: lambda para dashboard principal
   - `'director_home'`: lambda para dashboard director
   - `'teacher_home'`: lambda para dashboard profesor
   - `'parent_home'`: lambda para dashboard acudiente
   - `'show_frame'`: referencia directa a función `show_frame`
   - `'next'`: lambda que llama `next_step()`
   - `'prev'`: lambda que llama `prev_step()`
   - `'submit'`: lambda que llama `submit_form()`
3. Retorna el diccionario

**Estado global**: Variable global `nav_commands` contiene diccionario de comandos

**Siguiente**: PASO 9

---

#### **PASO 9: Creación de la Pantalla de Login**

**Archivo**: `app/ui/main.py` (línea 684-686)  
**Función**: `create_login_screen(main_frame)`  
**Evento**: Dentro de `initialize_app()`

```python
# app/ui/main.py, línea 684-686
frames["login"] = create_login_screen(main_frame)
frames["login"].grid(row=0, column=0, sticky="nsew")
print("DEBUG: login frame creado")
```

**Lo que hace `create_login_screen(parent_frame)` en línea 521-536**:

```python
def create_login_screen(parent_frame):
    """Crea la pantalla de login con columnas de autenticación y pre-inscripción"""
    login_layout = tk.Frame(parent_frame)
    login_layout.grid_columnconfigure(0, weight=1)
    login_layout.grid_columnconfigure(1, weight=1)
    login_layout.grid_rowconfigure(0, weight=1)
    
    login_column = create_login_column(login_layout, login_to_dashboard)
    login_column.grid(row=0, column=0, sticky="nsew")
    
    pre_column = create_pre_column(login_layout)
    pre_column.grid(row=0, column=1, sticky="nsew")

    return login_layout
```

**Acciones** en secuencia:

**9.1: Crear Frame de layout**
```python
login_layout = tk.Frame(parent_frame)  # Frame principal que contiene ambas columnas
```

**9.2: Configurar grid del layout**
```python
login_layout.grid_columnconfigure(0, weight=1)  # Columna 0 expandible
login_layout.grid_columnconfigure(1, weight=1)  # Columna 1 expandible
login_layout.grid_rowconfigure(0, weight=1)     # Fila 0 expandible
```

**9.3: Crear columna de login** → PASO 10

**9.4: Crear columna de pre-inscripción** → PASO 11

**9.5: Retornar el frame completo**
```python
return login_layout
```

**Estado**: Frame de login creado pero aún no visible

**Siguiente**: PASO 10

---

#### **PASO 10: Creación de la Columna de Autenticación**

**Archivo**: `app/ui/main.py` (línea 470-520)  
**Función**: `create_login_column(parent, login_command)`  
**Evento**: Llamada desde `create_login_screen()` en línea 528

```python
# app/ui/main.py, línea 470-520
def create_login_column(parent, login_command):
    """Crea la columna de login en la pantalla de autenticación"""
    global login_form
    
    column = tk.Frame(parent, bg=COLOR_BG_LOGIN)
```

**Acciones en detalle**:

**10.1: Crear frame de columna**
```python
column = tk.Frame(parent, bg=COLOR_BG_LOGIN)  # Frame contenedor
# bg=COLOR_BG_LOGIN es color de fondo (constante importada)
```

**10.2: Crear header con título**
```python
tk.Label(column, text="Sistema de Gestión Académica", 
         bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, 
         font=FONT_H1).pack(fill="x", side="top", ipady=30)
```
Crea etiqueta con título principal

**10.3: Crear subtítulo**
```python
tk.Label(column, text="Colegio Pequeño - Educación Inicial", 
         bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, 
         font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
```

**10.4: Crear contenedor principal**
```python
login_main_container = tk.Frame(column, bg=COLOR_BG_LOGIN)
login_main_container.pack(expand=True, fill="both")
```

**10.5: Crear frame centrado para formulario**
```python
login_main = tk.Frame(login_main_container, 
                     bg=COLOR_BG_LOGIN, width=350, height=450)
login_main.place(relx=0.5, rely=0.5, anchor="center")
login_main.pack_propagate(False)
```
Frame de tamaño fijo (350x450) centrado

**10.6: Crear etiqueta "Autenticación de Usuario"**
```python
tk.Label(login_main, text="Autenticación de Usuario", 
         bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, 
         font=FONT_H2).pack(anchor="w", pady=(0, 20))
```

**10.7: Crear instancia de LoginForm** → PASO 12

**10.8: Crear botón "Acceder"**
```python
ttk.Button(login_main, text="Acceder", style="Admin.TButton", 
           command=login_command).pack(fill="x", ipady=8)
```
Botón que ejecuta `login_to_dashboard` cuando se presiona

**10.9: Crear enlace "¿Olvidó su contraseña?"**
```python
recuperar_link = tk.Label(...)
recuperar_link.bind("<Button-1>", lambda e: abrir_recuperar_password())
```
Etiqueta clickeable que abre ventana de recuperación

**10.10: Mostrar usuarios de prueba (solo en desarrollo)**
```python
if IS_DEVELOPMENT and TEST_USERS_DISPLAY:
    for user_pass, role in TEST_USERS_DISPLAY:
        tk.Label(login_main, text=f"• {user_pass} ({role})", ...).pack()
```

**10.11: Retornar frame**
```python
return column
```

**Estado**: Columna de login creada con todos los componentes

**Siguiente**: PASO 12

---

#### **PASO 11: Creación de la Columna de Pre-inscripción**

**Archivo**: `app/ui/main.py` (línea 436-469)  
**Función**: `create_pre_column(parent)`  
**Evento**: Llamada desde `create_login_screen()` en línea 531

```python
def create_pre_column(parent):
    """Crea la columna de pre-inscripción en la pantalla de login"""
    column = tk.Frame(parent, bg=COLOR_ACCENT_DARK)
```

**Acciones en detalle**:

**11.1: Crear frame de columna**
```python
column = tk.Frame(parent, bg=COLOR_ACCENT_DARK)  # Fondo color accent
```

**11.2: Crear header "Pre-inscripción"**
```python
tk.Label(column, text="Pre-inscripción", bg=COLOR_ACCENT_DARK, 
         fg="#ffffff", font=FONT_H1).pack(fill="x", side="top", ipady=30)
```

**11.3: Crear subtítulo "Nuevo estudiante"**
```python
tk.Label(column, text="Nuevo estudiante", bg=COLOR_ACCENT_DARK, 
         fg="#ffffff", font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
```

**11.4: Crear contenedor principal**
```python
pre_main_container = tk.Frame(column, bg=COLOR_ACCENT_DARK)
pre_main_container.pack(expand=True, fill="both", padx=40, pady=40)
```

**11.5: Crear pregunta principal**
```python
tk.Label(pre_main_container, 
         text="¿Eres nuevo en nuestra institución?", 
         bg=COLOR_ACCENT_DARK, fg="#ffffff", 
         font=FONT_H2).pack(anchor="w", pady=(0, 20))
```

**11.6: Crear texto descriptivo**
```python
tk.Label(pre_main_container, 
         text="Completa el formulario de pre-inscripción...", 
         bg=COLOR_ACCENT_DARK, fg="#e0e0e0", 
         font=FONT_P, wraplength=350, 
         justify="left").pack(anchor="w", pady=(0, 40))
```

**11.7: Crear botón "Iniciar Pre-inscripción"**
```python
ttk.Button(pre_main_container, text="Iniciar Pre-inscripción", 
           style="Pre.TButton", 
           command=start_preinscription).pack(fill="x", ipady=10)
```
Botón que ejecuta `start_preinscription` cuando se presiona

**11.8: Crear sección de requisitos**
```python
tk.Label(pre_main_container, text="Requisitos:", ...).pack()
requisitos = [
    "✓ Documento de identidad del estudiante",
    "✓ Información de los acudientes",
    "✓ Historial académico anterior",
    "✓ Certificado de nacimiento"
]
for req in requisitos:
    tk.Label(pre_main_container, text=req, ...).pack()
```

**11.9: Retornar frame**
```python
return column
```

**Estado**: Columna de pre-inscripción creada con botón y requisitos

**Siguiente**: PASO 12

---

#### **PASO 12: Creación de Formulario de Login (Clase LoginForm)**

**Archivo**: `app/ui/components/login.py`  
**Clase**: `LoginForm`  
**Evento**: Instanciada en `create_login_column()` línea 497

```python
# app/ui/main.py, línea 497-504
login_form = LoginForm(login_main, {})
login_form.create_widgets(
    parent_frame=login_main,
    font=FONT_P,
    bg_color=COLOR_BG_LOGIN,
    placeholder_color=COLOR_TEXT_PLACEHOLDER,
    text_color=COLOR_TEXT_DARK
)
```

**Lo que hace el constructor `LoginForm.__init__()` en login.py**:

```python
class LoginForm:
    def __init__(self, parent: tk.Widget, config: dict):
        self.parent = parent
        self.config = config
        self._user_entry: tk.Entry = None
        self._pass_entry: tk.Entry = None
```

**Acciones**:

**12.1: Instanciar LoginForm**
```python
login_form = LoginForm(login_main, {})
# Asigna:
# - self.parent = login_main
# - self.config = {}
# - self._user_entry = None
# - self._pass_entry = None
```

**12.2: Llamar método `create_widgets()`**
```python
login_form.create_widgets(...)
```

**12.3: Lo que hace `create_widgets()` en login.py línea 14-24**:

```python
def create_widgets(self, parent_frame, font, bg_color, 
                  placeholder_color, text_color):
    # Campo Usuario
    tk.Label(parent_frame, text="Usuario:", bg=bg_color, 
             fg=text_color, font=font).pack(anchor="w")
    
    self._user_entry = tk.Entry(parent_frame, font=font, 
                                fg=placeholder_color, bg="#ffffff", bd=0)
    self._user_entry.pack(fill="x", pady=(0, 15), ipady=8)
    
    # Configurar placeholder para campo Usuario
    self._setup_placeholder(self._user_entry, 
                           "Ingrese su usuario", is_password=False)
    
    # Campo Contraseña
    tk.Label(parent_frame, text="Contraseña:", bg=bg_color, 
             fg=text_color, font=font).pack(anchor="w")
    
    self._pass_entry = tk.Entry(parent_frame, font=font, 
                                fg=placeholder_color, bg="#ffffff", bd=0)
    self._pass_entry.pack(fill="x", pady=(0, 20), ipady=8)
    
    # Configurar placeholder para campo Contraseña
    self._setup_placeholder(self._pass_entry, 
                           "Ingrese su contraseña", is_password=True)
```

**Acciones detalladas**:

**12.3.1: Crear etiqueta "Usuario:"**
```python
tk.Label(parent_frame, text="Usuario:", ...).pack(anchor="w")
```

**12.3.2: Crear Entry para usuario**
```python
self._user_entry = tk.Entry(parent_frame, ...)
self._user_entry.pack(fill="x", pady=(0, 15), ipady=8)
```

**12.3.3: Configurar placeholder de usuario**
```python
self._setup_placeholder(self._user_entry, "Ingrese su usuario", False)
```
Llama a `_setup_placeholder()` que:
- Asigna atributos al Entry: `placeholder`, `is_password`
- Crea funciones `on_focus_in()` y `on_focus_out()`
- Vincula eventos: `<FocusIn>` y `<FocusOut>`
- Cuando pierde foco, muestra placeholder en gris
- Cuando gana foco, borra placeholder y permite entrada

**12.3.4: Crear etiqueta "Contraseña:"**
```python
tk.Label(parent_frame, text="Contraseña:", ...).pack(anchor="w")
```

**12.3.5: Crear Entry para contraseña**
```python
self._pass_entry = tk.Entry(parent_frame, ...)
self._pass_entry.pack(fill="x", pady=(0, 20), ipady=8)
```

**12.3.6: Configurar placeholder de contraseña**
```python
self._setup_placeholder(self._pass_entry, "Ingrese su contraseña", True)
```
Similar a usuario pero con `is_password=True`:
- Cuando pierde foco: muestra placeholder sin asteriscos
- Cuando gana foco: borra placeholder y oculta entrada con asteriscos (`show="*"`)

**Estado global**: Variable global `login_form` contiene instancia de LoginForm

**Siguiente**: PASO 13

---

#### **PASO 13: Mostrar Pantalla de Login**

**Archivo**: `app/ui/main.py` (línea 689)  
**Función**: `show_frame("login")`  
**Evento**: Dentro de `initialize_app()` línea 689

```python
# app/ui/main.py, línea 689
show_frame("login")
```

**Lo que hace `show_frame()` en línea 89-227**:

```python
def show_frame(name):
    """Muestra el frame especificado y oculta los demás"""
    global step_index
    
    print(f"DEBUG: Intentando mostrar frame '{name}'")
    
    try:
        frame = frames.get(name)
        if frame is None:
            # ... carga dinámica
            return
        
        # Ocultar todos los frames
        for other_frame in frames.values():
            if other_frame and isinstance(other_frame, tk.Widget):
                other_frame.grid_remove()
        
        # Mostrar el frame solicitado
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Actualizar step_index
        if name == "login":
            step_index = -1
```

**Acciones**:

**13.1: Obtener frame de diccionario**
```python
frame = frames.get("login")
# Retorna el frame creado en PASO 9
```

**13.2: Ocultar todos los frames**
```python
for other_frame in frames.values():
    if other_frame and isinstance(other_frame, tk.Widget):
        other_frame.grid_remove()
```
Usa `grid_remove()` para ocultar (no destruir) todos los frames

**13.3: Mostrar frame de login**
```python
frame.grid(row=0, column=0, sticky="nsew")
```
Posiciona frame en grid con sticky="nsew" para expandir

**13.4: Actualizar step_index**
```python
if name == "login":
    step_index = -1
```

**Estado visual**: Pantalla de login ahora es visible en la ventana

**Siguiente**: PASO 14

---

#### **PASO 14: Inicio del Main Loop de Tkinter**

**Archivo**: `run_app.py` (línea 30)  
**Función**: `tk.Tk.mainloop()`  
**Evento**: Después de `initialize_app()` completado

```python
# run_app.py, línea 30
root_window.mainloop()
```

**Acciones**:

1. **Inicia el event loop de Tkinter**
   - Entra en bucle infinito esperando eventos
   - Procesa eventos del usuario (clics, teclas, movimientos del ratón)
   - Redibuja la ventana cuando es necesario
   - Nunca retorna hasta que se cierre la ventana

2. **Pantalla queda esperando**
   - Usuario ve pantalla de login completamente cargada
   - Puede escribir en campo de Usuario
   - Puede escribir en campo de Contraseña
   - Puede hacer clic en botón "Acceder"
   - Puede hacer clic en "¿Olvidó su contraseña?"
   - Puede hacer clic en "Iniciar Pre-inscripción"

**Estado final**: Sistema en espera de interacción del usuario

---

## Flujo Visual ASCII

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO APLICACIÓN                             │
│                  (run_app.py ejecutado)                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 1: Crear tk.Tk() → ventana raíz (root_window)             │
│  PASO 2: Cargar variables de entorno (.env)                     │
│  PASO 3: Inicializar mapeos ORM (SQLAlchemy)                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  initialize_app(root_window)                                    │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 4: Configurar ventana                          │        │
│  │  - Título: "Sistema de Gestión Académica"          │        │
│  │  - Tamaño: 1400x800 píxeles                         │        │
│  │  - Grid: Expandible en ambas direcciones            │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 5: Importar módulos                            │        │
│  │  - config (constantes)                              │        │
│  │  - styles (estilos)                                 │        │
│  │  - components (LoginForm, etc)                      │        │
│  │  - services (auth, rbac)                            │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 6: Aplicar estilos Tkinter                     │        │
│  │  - configure_styles() → define Admin.TButton        │        │
│  │                      → define Pre.TButton           │        │
│  │                      → define otros estilos         │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 7: Crear main_frame                            │        │
│  │  - tk.Frame en grid (0,0)                           │        │
│  │  - Expandible en ambas direcciones                  │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 8: Crear nav_commands (diccionario)            │        │
│  │  - 'home', 'logout', 'show_frame', etc.             │        │
│  │  - Usado para navegación entre pantallas            │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 9: Crear pantalla de login                     │        │
│  │  create_login_screen(main_frame)                    │        │
│  │  ┌────────────────────────────────────────┐        │        │
│  │  │ PASO 10: Columna de Autenticación     │        │        │
│  │  │  create_login_column()                │        │        │
│  │  │  ┌──────────────────────────────────┐ │        │        │
│  │  │  │ PASO 12: LoginForm               │ │        │        │
│  │  │  │  - Entry para usuario            │ │        │        │
│  │  │  │  - Entry para contraseña         │ │        │        │
│  │  │  │  - Placeholders funcionables     │ │        │        │
│  │  │  │  - Botón "Acceder"               │ │        │        │
│  │  │  │  - Link "¿Olvidó contraseña?"    │ │        │        │
│  │  │  └──────────────────────────────────┘ │        │        │
│  │  └────────────────────────────────────────┘        │        │
│  │  ┌────────────────────────────────────────┐        │        │
│  │  │ PASO 11: Columna de Pre-inscripción   │        │        │
│  │  │  create_pre_column()                   │        │        │
│  │  │  - Título "Pre-inscripción"            │        │        │
│  │  │  - Botón "Iniciar Pre-inscripción"     │        │        │
│  │  │  - Lista de requisitos                 │        │        │
│  │  └────────────────────────────────────────┘        │        │
│  └─────────────────────────────────────────────────────┘        │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ PASO 13: Mostrar frame de login                     │        │
│  │  show_frame("login")                                │        │
│  │  - Oculta otros frames (si los hay)                 │        │
│  │  - Posiciona frame de login en grid                 │        │
│  │  - Frame se vuelve visible                          │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  PASO 14: root_window.mainloop()                                │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ EVENTO LOOP INICIADO - Sistema esperando eventos   │        │
│  │                                                     │        │
│  │ La aplicación queda en espera de:                   │        │
│  │  • Click en "Acceder" → login_to_dashboard()        │        │
│  │  • Click en "¿Olvidó?" → abrir_recuperar_password()│        │
│  │  • Click en "Pre-inscripción" → start_preinscription│        │
│  │  • Cierre de ventana → exit                         │        │
│  │  • Movimientos del ratón → redibuja                 │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estados Finales

### Estado de Variables Globales

| Variable | Tipo | Valor | Descripción |
|----------|------|-------|------------|
| `root` | `tk.Tk` | Ventana principal | Ventana raíz de la aplicación |
| `main_frame` | `tk.Frame` | Frame contenedor | Frame principal que contiene todos los frames |
| `frames` | `dict` | `{"login": <frame>}` | Diccionario de frames disponibles |
| `nav_commands` | `dict` | `{10 comandos}` | Diccionario de comandos de navegación |
| `login_form` | `LoginForm` | Instancia | Objeto con campos de entrada de credenciales |
| `auth_service` | `AuthenticationService` | Instancia | Servicio de autenticación (no usado aún) |
| `step_index` | `int` | `-1` | Índice actual en formulario de pre-inscripción |

### Componentes Visuales en Pantalla

```
┌──────────────────────────────────────────────────────────────┐
│                  PANTALLA DE LOGIN FINAL                      │
├────────────────────────┬────────────────────────────────────┤
│                        │                                      │
│  COLUMNA IZQUIERDA     │    COLUMNA DERECHA                  │
│  (Autenticación)       │    (Pre-inscripción)                │
│                        │                                      │
│  - Título principal    │    - Título "Pre-inscripción"      │
│  - Subtítulo           │    - Pregunta "¿Nuevo?"            │
│  - Campo "Usuario"     │    - Descripción                    │
│  - Campo "Contraseña"  │    - Botón "Iniciar"              │
│  - Botón "Acceder"     │    - Requisitos listados            │
│  - Link recuperar      │                                      │
│  - Usuarios de prueba  │                                      │
│                        │                                      │
└────────────────────────┴────────────────────────────────────┘
```

### Archivos Cargados en Memoria

```
✓ run_app.py                        - Script principal
✓ app/ui/main.py                   - Lógica de UI
✓ app/ui/config.py                 - Constantes
✓ app/ui/styles.py                 - Estilos Tkinter
✓ app/ui/components/login.py       - LoginForm
✓ app/services/auth_service.py     - Servicio de auth
✓ app/services/rbac_service.py     - Control de acceso
✓ app/data/mappers.py              - Mapeos ORM
✓ .env                             - Variables de entorno
✓ Todos los módulos importados por los anteriores
```

### Servicios Listos pero No Inicializados

| Servicio | Estado | Inicialización |
|----------|--------|----------------| 
| AuthenticationService | Cargado | Espera login |
| RBAC Service | Cargado | Espera login |
| Database Session | Cargado | Espera consulta |
| Email Service | No cargado | Bajo demanda |
| Reportes | No cargado | Bajo demanda |

---

## Resumen de Clases y Responsabilidades

### Clases de Presentación (UI)

| Clase | Archivo | Responsabilidad | Instancias |
|-------|---------|-----------------|-----------|
| `tk.Tk` | tkinter | Ventana raíz | 1 (root) |
| `tk.Frame` | tkinter | Frames contenedores | 5+ |
| `tk.Label` | tkinter | Etiquetas de texto | 20+ |
| `tk.Entry` | tkinter | Campos de entrada | 2 |
| `ttk.Button` | tkinter.ttk | Botones estilizados | 3+ |
| `LoginForm` | app.ui.components | Formulario login | 1 |

### Clases de Servicios

| Clase | Archivo | Estado |
|-------|---------|--------|
| `AuthenticationService` | app.services | Instanciada, no usada |
| `RBACService` | app.services | Instanciada, no usada |
| `SessionLocal` | app.config.database | Disponible, no usada |

### Funciones de Control

| Función | Archivo | Responsabilidad |
|---------|---------|-----------------|
| `initialize_app()` | app/ui/main.py | Inicializa toda la UI |
| `show_frame()` | app/ui/main.py | Muestra/oculta frames |
| `create_login_screen()` | app/ui/main.py | Crea pantalla login |
| `create_login_column()` | app/ui/main.py | Crea columna auth |
| `create_pre_column()` | app/ui/main.py | Crea columna pre-inscrip |
| `login_to_dashboard()` | app/ui/main.py | Maneja login (no ejecutado) |
| `start_preinscription()` | app/ui/main.py | Inicia pre-inscrip (no ejecutado) |
| `configure_styles()` | app/ui/styles.py | Aplica estilos |

---

**Diagrama creado**: 12 de Diciembre 2025  
**Versión**: 1.0  
**Próximo diagrama**: Flujo de Login (CU-01: Iniciar Sesión)
