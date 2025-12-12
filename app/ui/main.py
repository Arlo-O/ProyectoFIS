import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import sys
from typing import Optional
from dotenv import load_dotenv


load_dotenv()


try:
    from .config import *
    from .styles import configure_styles
    from .components.session import set_current_role, set_user_info, clear_session
    from .components.login import LoginForm
    from .components.recuperar_password import RecuperarPasswordWindow
    from app.services.auth_service import AuthenticationService
    from app.services.rbac_service import rbac_service
    from .components.form import create_step1, create_step2, create_step3, create_step4
    # ✅ NO CARGAR MÓDULOS AQUÍ - Se cargan bajo demanda después de login
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import *
    from styles import configure_styles
    from components.session import set_current_role, set_user_info, clear_session
    from components.login import LoginForm
    from components.recuperar_password import RecuperarPasswordWindow
    from app.services.auth_service import AuthenticationService
    from app.services.rbac_service import rbac_service
    from components.form import create_step1, create_step2, create_step3, create_step4
    # ✅ NO CARGAR MÓDULOS AQUÍ - Se cargan bajo demanda después de login
    from modules.reports import create_report_generator



root = None
main_frame = None
frames = {}
step_index = -1
login_form: Optional[LoginForm] = None
auth_service: AuthenticationService = AuthenticationService()
nav_commands = {}


# Cargar usuarios de prueba desde .env (solo desarrollo)
IS_DEVELOPMENT = os.getenv("ENVIRONMENT", "development").lower() == "development"


TEST_USERS_DISPLAY = []
if IS_DEVELOPMENT:
    TEST_USERS_DISPLAY = [
        (f"{os.getenv('TEST_ADMIN_EMAIL', 'admin@colegio.edu')} / {os.getenv('TEST_ADMIN_PASSWORD', 'admin123')}", "Administrador"),
        (f"{os.getenv('TEST_DIRECTOR_EMAIL', 'director@colegio.edu')} / {os.getenv('TEST_DIRECTOR_PASSWORD', 'dir123')}", "Director"),
        (f"{os.getenv('TEST_TEACHER_EMAIL', 'profesor@colegio.edu')} / {os.getenv('TEST_TEACHER_PASSWORD', 'prof123')}", "Profesor"),
        (f"{os.getenv('TEST_PARENT_EMAIL', 'padre@colegio.edu')} / {os.getenv('TEST_PARENT_PASSWORD', 'papa123')}", "Acudiente")
    ]



def setup_placeholder(entry, placeholder, is_password=False):
    """Configura el comportamiento de placeholder en un Entry"""
    entry.placeholder = placeholder
    entry.is_password = is_password
    
    def on_focus_in(event):
        if entry.get() == entry.placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=COLOR_TEXT_DARK)
            if entry.is_password:
                entry.config(show="*")
                
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, entry.placeholder)
            entry.config(fg=COLOR_TEXT_PLACEHOLDER)
            if entry.is_password:
                entry.config(show="")
    
    on_focus_out(None)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)



def show_frame(name):
    """Muestra el frame especificado y oculta los demás"""
    global step_index
    
    print(f"DEBUG: Intentando mostrar frame '{name}'")
    print(f"DEBUG: Frames disponibles: {list(frames.keys())}")
    
    try:
        frame = frames.get(name)
        if frame is None:
            # ✅ Intentar carga dinámica de módulos del director
            if name == 'aspirantes_manager':
                print(f"DEBUG: Cargando módulo de aspirantes dinámicamente...")
                from .modules.aspirantes import create_aspirantes_manager
                
                # Obtener el main_frame correctamente
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_aspirantes_manager(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de aspirantes creado exitosamente")
            elif name == 'achievements_manager':
                print(f"DEBUG: Cargando módulo de logros dinámicamente...")
                from .modules.achievements import create_achievements_manager
                
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_achievements_manager(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de logros creado exitosamente")
            elif name == 'student_manager':
                print(f"DEBUG: Cargando módulo de estudiantes dinámicamente...")
                from .modules.student import create_student_manager
                
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_student_manager(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de estudiantes creado exitosamente")
            elif name == 'groups_manager':
                print(f"DEBUG: Cargando módulo de grupos dinámicamente...")
                from .modules.groups import create_groups_manager
                
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_groups_manager(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de grupos creado exitosamente")
            elif name == 'citation_generator':
                print(f"DEBUG: Cargando módulo de citaciones dinámicamente...")
                from .modules.citations import create_citation_generator
                
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_citation_generator(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de citaciones creado exitosamente")
            elif name == 'evaluations_manager':
                print(f"DEBUG: Cargando módulo de evaluaciones dinámicamente...")
                from .modules.evaluations import create_evaluations_manager
                
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                frame = create_evaluations_manager(main_frame_widget, nav_commands)
                frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"DEBUG: ✅ Módulo de evaluaciones creado exitosamente")
            else:
                print(f"ERROR: El frame '{name}' no existe!")
                messagebox.showerror("Error", f"El frame '{name}' no se pudo cargar.")
                return
        
        # ✅ IMPORTANTE: Verificar que frame es realmente un Tk widget
        if not isinstance(frame, tk.Widget):
            print(f"ERROR: El frame '{name}' no es un Widget válido, es: {type(frame)}")
            messagebox.showerror("Error", f"El frame '{name}' no es válido: {type(frame)}")
            return
        
        # Ocultar todos los frames
        for other_frame in frames.values():
            if other_frame and isinstance(other_frame, tk.Widget):
                other_frame.grid_remove()
        
        # Mostrar el frame solicitado
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Actualizar step_index según el frame mostrado
        if name == "login":
            step_index = -1
        elif name.startswith("step"):
            step_num = int(name.replace("step", ""))
            step_index = step_num - 1
            print(f"DEBUG: step_index actualizado a {step_index}")
            
    except Exception as e:
        import traceback
        print(f"Error en show_frame('{name}'): {str(e)}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Error al mostrar frame {name}: {str(e)}")



def abrir_recuperar_password():
    """
    Paso 1 del CU-07: Usuario hace clic en "¿Olvidó su contraseña?"
    Abre la ventana de recuperación de contraseña
    """
    try:
        # Obtener la ventana raíz
        global main_frame
        root = main_frame.winfo_toplevel()
        
        # Crear y mostrar ventana de recuperación
        RecuperarPasswordWindow(root)
    
    except Exception as e:
        import traceback
        print(f"Error al abrir recuperar contraseña: {str(e)}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Error al abrir recuperación de contraseña: {str(e)}")


def start_preinscription():
    """Inicia el proceso de pre-inscripción"""
    try:
        print("DEBUG: Iniciando pre-inscripción")
        
        # ✅ Crear el frame de preinscripción si no existe
        global frames, main_frame, nav_commands
        
        if "step1" not in frames:
            print("DEBUG: Creando frame de preinscripción")
            # Crear el frame unificado de preinscripción
            frames["step1"] = create_step1(main_frame, nav_commands)
            frames["step1"].grid(row=0, column=0, sticky="nsew")
        
        show_frame("step1")
    except Exception as e:
        import traceback
        print(f"Error en start_preinscription: {str(e)}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Error al iniciar pre-inscripción: {str(e)}")



def next_step():
    """Avanza al siguiente paso del formulario"""
    global step_index
    print(f"DEBUG: next_step() - step_index actual: {step_index}")
    
    if step_index < 3:
        step_index += 1
        show_frame(f"step{step_index + 1}")
    else:
        messagebox.showinfo("Información", "Ya estás en el último paso.")



def prev_step():
    """Retrocede al paso anterior del formulario"""
    global step_index
    print(f"DEBUG: prev_step() - step_index actual: {step_index}")
    
    if step_index > 0:
        step_index -= 1
        show_frame(f"step{step_index + 1}")
    elif step_index == 0:
        step_index = -1
        show_frame("login")
    else:
        show_frame("login")



def login_to_dashboard():
    """
    Controlador del evento de login.
    Crea dinámicamente el dashboard apropiado solo después de autenticación exitosa.
    """
    global login_form
    
    if login_form is None:
        messagebox.showerror("Error", "La interfaz de login no se ha inicializado correctamente.")
        return
    
    # Verificar que los campos no estén vacíos
    if login_form.is_empty():
        messagebox.showerror("Error de Login", "Por favor, ingrese usuario y contraseña.")
        return
    
    # Obtener credenciales del formulario
    user_email, password = login_form.get_credentials()
    
    # Validar formato de credenciales
    is_valid, error_msg = auth_service.validate_credentials(user_email, password)
    if not is_valid:
        messagebox.showerror("Error de validación", error_msg)
        return
    
    try:
        # Autenticar contra la BD
        usuario = auth_service.authenticate(user_email, password)
        
        if usuario is None:
            messagebox.showerror("Error de Login", "Credenciales incorrectas.")
            return
        
        # ✅ Obtener rol (ya debe estar cargado en authenticate())
        try:
            rol = usuario.rol
            if rol is None:
                messagebox.showerror("Error de Rol", "El usuario no tiene un rol asignado.")
                return
            
            role_name = rol.nombre_rol.lower() if hasattr(rol, 'nombre_rol') else str(rol).lower()
        except Exception as e:
            print(f"ERROR obteniendo rol: {e}")
            messagebox.showerror("Error de Rol", f"Error al obtener rol del usuario: {str(e)}")
            return
        
        # ✅ Obtener permisos del usuario (cargados en authenticate())
        permisos = getattr(usuario, '_permisos', [])
        print(f"[LOGIN] Usuario: {usuario.correo_electronico}, Rol: {role_name}, Permisos: {permisos}")
        
        # ✅ Configurar contexto RBAC con usuario y permisos
        rbac_service.set_user_context(usuario, role_name, permisos)
        
        # Obtener nombre de la persona asociada
        persona = getattr(usuario, 'persona', None)
        if persona and hasattr(persona, 'primer_nombre'):
            nombre_completo = f"{persona.primer_nombre} {persona.primer_apellido}"
        else:
            nombre_completo = usuario.correo_electronico
        
        # Guardar info en sesión
        set_user_info(
            user_id=usuario.id_usuario,
            name=nombre_completo,
            email=usuario.correo_electronico,
            role=role_name,
            department=None
        )
        
        # ✅ Mapear rol a módulo y crear SOLO el dashboard autorizado
        # Las importaciones se hacen aquí, DESPUÉS de validar el rol
        dashboard_creator_map = {}
        
        if role_name == "administrador":
            from .modules.admin import create_admin_dashboard
            dashboard_creator_map["administrador"] = ("dashboard", create_admin_dashboard)
        elif role_name == "director":
            from .modules.director import create_director_dashboard
            dashboard_creator_map["director"] = ("director_dashboard", create_director_dashboard)
        elif role_name == "profesor":
            from .modules.teacher import create_teacher_dashboard
            dashboard_creator_map["profesor"] = ("teacher_dashboard", create_teacher_dashboard)
        elif role_name == "acudiente":
            from .modules.parent import create_parent_dashboard
            dashboard_creator_map["acudiente"] = ("parent_dashboard", create_parent_dashboard)
        else:
            messagebox.showerror("Error de Rol", f"Rol '{role_name}' no tiene dashboard asignado.")
            return
        
        dashboard_info = dashboard_creator_map.get(role_name)
        if not dashboard_info:
            messagebox.showerror("Error de Rol", f"Rol '{role_name}' no tiene dashboard asignado.")
            return
        
        frame_name, dashboard_creator = dashboard_info
        
        # ✅ Crear el dashboard SOLO AHORA si no existe
        if frame_name not in frames or frames[frame_name] is None:
            print(f"[LOGIN] Creando dashboard: {frame_name} para rol: {role_name}")
            try:
                # Obtener el main_frame correctamente
                for widget in root.winfo_children():
                    if isinstance(widget, tk.Frame):
                        main_frame_widget = widget
                        break
                else:
                    raise Exception("No se encontró el main_frame")
                
                # Crear dashboard
                dashboard_frame = dashboard_creator(main_frame_widget, nav_commands)
                
                if dashboard_frame is None:
                    raise Exception(f"La función {dashboard_creator.__name__} retornó None")
                
                frames[frame_name] = dashboard_frame
                dashboard_frame.grid(row=0, column=0, sticky="nsew")
                print(f"[LOGIN] ✅ Dashboard creado exitosamente: {frame_name}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el dashboard: {str(e)}")
                print(f"ERROR creando dashboard {frame_name}: {e}")
                import traceback
                traceback.print_exc()
                return
        
        # Mostrar el dashboard del usuario
        show_frame(frame_name)
        login_form.clear()
        
        # Obtener nombre para mostrar
        nombre_usuario = getattr(usuario, 'primer_nombre', None) or usuario.correo_electronico
        messagebox.showinfo("Éxito", f"¡Bienvenido, {nombre_usuario}!\n\nRol: {role_name}\nPermisos: {len(permisos)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante el login: {str(e)}")
        print(f"Error en login_to_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()



def create_pre_column(parent):
    """Crea la columna de pre-inscripción en la pantalla de login"""
    column = tk.Frame(parent, bg=COLOR_ACCENT_DARK)
    
    tk.Label(column, text="Pre-inscripción", bg=COLOR_ACCENT_DARK, fg="#ffffff", font=FONT_H1).pack(fill="x", side="top", ipady=30)
    tk.Label(column, text="Nuevo estudiante", bg=COLOR_ACCENT_DARK, fg="#ffffff", font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
    
    pre_main_container = tk.Frame(column, bg=COLOR_ACCENT_DARK)
    pre_main_container.pack(expand=True, fill="both", padx=40, pady=40)
    
    tk.Label(pre_main_container, text="¿Eres nuevo en nuestra institución?", bg=COLOR_ACCENT_DARK, fg="#ffffff", font=FONT_H2).pack(anchor="w", pady=(0, 20))
    
    tk.Label(pre_main_container, text="Completa el formulario de pre-inscripción para registrar a tu hijo(a) en nuestro colegio.", bg=COLOR_ACCENT_DARK, fg="#e0e0e0", font=FONT_P, wraplength=350, justify="left").pack(anchor="w", pady=(0, 40))
    
    ttk.Button(pre_main_container, text="Iniciar Pre-inscripción", style="Pre.TButton", command=start_preinscription).pack(fill="x", ipady=10)
    
    tk.Label(pre_main_container, text="", bg=COLOR_ACCENT_DARK).pack(pady=20)
    
    tk.Label(pre_main_container, text="Requisitos:", bg=COLOR_ACCENT_DARK, fg="#ffffff", font=FONT_H3).pack(anchor="w", pady=(0, 10))
    
    requisitos = [
        "✓ Documento de identidad del estudiante",
        "✓ Información de los acudientes",
        "✓ Historial académico anterior",
        "✓ Certificado de nacimiento"
    ]
    
    for req in requisitos:
        tk.Label(pre_main_container, text=req, bg=COLOR_ACCENT_DARK, fg="#e0e0e0", font=FONT_P).pack(anchor="w", pady=5)
    
    return column



def create_login_column(parent, login_command):
    """Crea la columna de login en la pantalla de autenticación"""
    global login_form
    
    column = tk.Frame(parent, bg=COLOR_BG_LOGIN)
    tk.Label(column, text="Sistema de Gestión Académica", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_H1).pack(fill="x", side="top", ipady=30)
    tk.Label(column, text="Colegio Pequeño - Educación Inicial", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
    
    login_main_container = tk.Frame(column, bg=COLOR_BG_LOGIN)
    login_main_container.pack(expand=True, fill="both")

    login_main = tk.Frame(login_main_container, bg=COLOR_BG_LOGIN, width=350, height=450)
    login_main.place(relx=0.5, rely=0.5, anchor="center")
    login_main.pack_propagate(False)
    
    tk.Label(login_main, text="Autenticación de Usuario", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_H2).pack(anchor="w", pady=(0, 20))
    
    # Crear instancia de LoginForm
    login_form = LoginForm(login_main, {})
    login_form.create_widgets(
        parent_frame=login_main,
        font=FONT_P,
        bg_color=COLOR_BG_LOGIN,
        placeholder_color=COLOR_TEXT_PLACEHOLDER,
        text_color=COLOR_TEXT_DARK
    )
    
    ttk.Button(login_main, text="Acceder", style="Admin.TButton", command=login_command).pack(fill="x", ipady=8)
    
    # Paso 1 del CU-07: Enlace "¿Olvidó su contraseña?"
    recuperar_link = tk.Label(
        login_main,
        text="¿Olvidó su contraseña?",
        bg=COLOR_BG_LOGIN,
        fg="#3498db",
        font=("Segoe UI", 9, "underline"),
        cursor="hand2"
    )
    recuperar_link.pack(pady=(10, 0))
    recuperar_link.bind("<Button-1>", lambda e: abrir_recuperar_password())
    
    tk.Label(login_main, text="Usuarios de prueba:", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(20, 10))
    
    if IS_DEVELOPMENT and TEST_USERS_DISPLAY:
        for user_pass, role in TEST_USERS_DISPLAY:
            tk.Label(login_main, text=f"• {user_pass} ({role})", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
    
    return column



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



def extract_frame_from_result(result, step_name):
    """
    ✅ SOLUCIÓN: Extrae el frame de lo que retorna create_step()
    
    Algunos módulos retornan tuplas (frame, canvas, etc) en lugar de solo el frame.
    Esta función maneja ambos casos.
    """
    if result is None:
        print(f"ERROR: create_{step_name} retornó None")
        return None
    
    # Si es una tupla, tomar el primer elemento (debería ser el frame)
    if isinstance(result, tuple):
        print(f"DEBUG: {step_name} retornó tupla, extrayendo primer elemento")
        frame = result[0]
        if isinstance(frame, tk.Widget):
            return frame
        else:
            print(f"ERROR: Primer elemento de tupla no es un Widget: {type(frame)}")
            return None
    
    # Si ya es un frame, devolverlo directamente
    if isinstance(result, tk.Widget):
        return result
    
    print(f"ERROR: Tipo inesperado para {step_name}: {type(result)}")
    return None



def create_step_screen(parent_frame, step_num, creation_func, nav_cmds):
    """
    Crea un frame de paso del formulario de pre-inscripción
    
    Args:
        parent_frame: Frame padre donde se creará el paso
        step_num: Número del paso (1-4)
        creation_func: Función que crea el contenido del paso
        nav_cmds: Diccionario de comandos de navegación
    
    Returns:
        Frame del paso creado
    """
    try:
        print(f"DEBUG: Creando step{step_num}")
        
        if creation_func is None:
            raise ValueError(f"creation_func para step{step_num} es None")
        
        # Pasar nav_commands a la función de creación
        result = creation_func(parent_frame, nav_cmds)
        
        # ✅ Extraer el frame del resultado (maneja tuplas)
        step_frame = extract_frame_from_result(result, f"step{step_num}")
        
        if step_frame is None:
            raise ValueError(f"create_step{step_num} no creó un frame válido")
        
        print(f"DEBUG: step{step_num} creado correctamente")
        return step_frame
        
    except Exception as e:
        print(f"Error en create_step_screen para el paso {step_num}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise



def logout():
    """
    Realiza logout del usuario y limpia la sesión
    """
    global login_form
    try:
        # Limpiar contexto RBAC
        rbac_service.limpiar_contexto()
        
        # Limpiar información de sesión
        clear_session()
        
        print("[LOGOUT] Sesión cerrada correctamente")
        
        # Mostrar pantalla de login
        show_frame("login")
        
        if login_form:
            login_form.clear()
            
    except Exception as e:
        print(f"Error en logout: {e}")
        import traceback
        traceback.print_exc()


def create_nav_commands():
    """Crea el diccionario de comandos de navegación para todos los módulos"""
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



def submit_form():
    """Maneja el envío del formulario de pre-inscripción"""
    try:
        # Aquí iría la lógica para enviar datos a la base de datos
        messagebox.showinfo("Éxito", "Formulario enviado correctamente")
        print("DEBUG: Formulario enviado")
        # Después de enviar, volver al login
        show_frame("login")
    except Exception as e:
        messagebox.showerror("Error", f"Error al enviar formulario: {str(e)}")
        print(f"Error en submit_form: {str(e)}")



def initialize_app(root_window):
    """
    Inicializa la aplicación y crea SOLO la pantalla de login inicialmente.
    Los dashboards se crean después del login, solo si el usuario tiene permisos.
    
    Args:
        root_window: Ventana raíz de Tkinter
    """
    global root, frames, nav_commands, main_frame
    
    root = root_window
    root.title("Sistema de Gestión Académica")
    root.geometry("1400x800")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    configure_styles(root_window)

    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    
    # ✅ Crear nav_commands PRIMERO, antes de crear los frames
    nav_commands = create_nav_commands()
    print("DEBUG: nav_commands creado")
    
    print("DEBUG: Inicializando frames...")
    
    # ✅ SOLO crear pantalla de login y pre-inscripción inicialmente
    frames["login"] = create_login_screen(main_frame)
    frames["login"].grid(row=0, column=0, sticky="nsew")
    print("DEBUG: login frame creado")
    
    # Mostrar la pantalla de login como pantalla inicial
    show_frame("login")
    
    # Los dashboards se crean bajo demanda cuando el usuario hace login exitoso
    print("DEBUG: Inicialización completada. Sistema listo.")
    
    print("DEBUG: Todos los frames inicializados")
    print(f"DEBUG: Frames creados: {list(frames.keys())}")
    
    # Mostrar pantalla de login
    show_frame("login")



if __name__ == "__main__":
    root_window = tk.Tk()
    initialize_app(root_window)
    root_window.mainloop()