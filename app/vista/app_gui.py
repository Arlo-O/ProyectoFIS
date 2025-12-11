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
    from .gui_styles import configure_styles
    from .session_manager import set_current_role, set_user_info
    from .login_form import LoginForm
    from .auth_service import AuthenticationService
    from .formGui import create_step1, create_step2, create_step3, create_step4
    from .moduloAdmin import create_admin_dashboard
    from .moduloDirectivo import create_director_dashboard
    from .moduloProfesor import create_teacher_dashboard, create_assignment_teacher, create_observer_teacher
    from .moduloAcudiente import create_parent_dashboard, create_consult_parent
    from .moduloCitacion import create_citation_generator
    from .moduloGrupos import create_groups_manager
    from .moduloLogros import create_achievements_manager
    from .moduloEstudiantes import create_student_manager
    from .moduloEvaluaciones import create_evaluations_manager
    from .moduloCursosAsignados import create_assigned_courses
    from .moduloBoletines import create_report_generator
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import *
    from gui_styles import configure_styles
    from session_manager import set_current_role, set_user_info
    from login_form import LoginForm
    from auth_service import AuthenticationService
    from formGui import create_step1, create_step2, create_step3, create_step4
    from moduloAdmin import create_admin_dashboard
    from moduloDirectivo import create_director_dashboard
    from moduloProfesor import create_teacher_dashboard, create_assignment_teacher, create_observer_teacher
    from moduloAcudiente import create_parent_dashboard, create_consult_parent
    from moduloCitacion import create_citation_generator
    from moduloGrupos import create_groups_manager
    from moduloLogros import create_achievements_manager
    from moduloEstudiantes import create_student_manager
    from moduloEvaluaciones import create_evaluations_manager
    from moduloCursosAsignados import create_assigned_courses
    from moduloBoletines import create_report_generator


root = None
frames = {}
step_index = -1
step_canvases = {}
login_form: Optional[LoginForm] = None
auth_service: AuthenticationService = AuthenticationService()

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
    global step_index
    
    frame = frames.get(name)
    if frame:
        for other_frame in frames.values():
            other_frame.grid_remove()
        
        frame.grid(row=0, column=0, sticky="nsew")
        
        if name == "login":
            step_index = -1
        elif name.startswith("step"):
            new_index = int(name.replace("step", "")) - 1
            step_index = new_index
            if name in step_canvases:
                canvas = step_canvases[name]['canvas']
                root.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(0)


def start_preinscription():
    show_frame("step1")


def next_step():
    global step_index
    if step_index < 3:
        show_frame(f"step{step_index + 2}")


def prev_step():
    global step_index
    if step_index > 0:
        show_frame(f"step{step_index}")
    elif step_index == 0:
        show_frame("login")


def login_to_dashboard():
    """
    Controlador del evento de login.
    Valida credenciales usando AuthenticationService y SessionManager,
    luego navega al dashboard correspondiente según el rol del usuario.
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
        
        role = getattr(usuario, 'rol', None)
        if role is None:
            messagebox.showerror("Error de Rol", "El usuario no tiene un rol asignado.")
            return
        
        role_name = role.nombre_rol.lower() if hasattr(role, 'nombre_rol') else str(role).lower()
        
        # Guardar info en sesión
        set_user_info(
            user_id=usuario.id_usuario,
            name=f"{usuario.primer_nombre} {usuario.primer_apellido}",
            email=usuario.correo_electronico,
            role=role_name,
            department=None
        )
        
        # Mapear rol a frame
        role_map = {
            "administrador": "dashboard",
            "director": "director_dashboard",
            "profesor": "teacher_dashboard",
            "acudiente": "parent_dashboard",
        }
        
        target_frame = role_map.get(role_name)
        if target_frame:
            show_frame(target_frame)
            login_form.clear()
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario.primer_nombre}!")
        else:
            messagebox.showerror("Error de Rol", f"Rol '{role_name}' no tiene dashboard asignado.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante el login: {str(e)}")
        print(f"Error en login_to_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()


def create_pre_column(parent):
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
    
    tk.Label(login_main, text="Usuarios de prueba:", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(20, 10))
    
    test_users = [
        ("admin@colegio.edu / admin123", "Administrador"),
        ("director@colegio.edu / dir123", "Director"),
        ("profesor@colegio.edu / prof123", "Profesor"),
        ("padre@colegio.edu / papa123", "Acudiente")
    ]
    
    for user_pass, role in test_users:
        tk.Label(login_main, text=f"• {user_pass} ({role})", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack(anchor="w")
    
    return column


def create_login_screen(parent_frame):
    login_layout = tk.Frame(parent_frame)
    login_layout.grid_columnconfigure(0, weight=1)
    login_layout.grid_columnconfigure(1, weight=1)
    login_layout.grid_rowconfigure(0, weight=1)
    
    login_column = create_login_column(login_layout, login_to_dashboard)
    login_column.grid(row=0, column=0, sticky="nsew")
    
    pre_column = create_pre_column(login_layout)
    pre_column.grid(row=0, column=1, sticky="nsew")

    return login_layout

def create_step_screen(parent_frame, step_num, creation_func):
    step_frame = tk.Frame(parent_frame, bg="#f5f7fa")
    
    canvas = tk.Canvas(step_frame, bg="#f5f7fa", highlightthickness=0)
    scrollbar = ttk.Scrollbar(step_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f7fa")
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    step_canvases[f"step{step_num}"] = {'canvas': canvas, 'frame': scrollable_frame}
    
    nav_commands = create_nav_commands()
    content = creation_func(scrollable_frame, nav_commands)
    
    return step_frame



def create_nav_commands():
    nav_commands = {
        'home': lambda: show_frame("login"),
        'dashboard_home': lambda: show_frame("dashboard"),
        'director_home': lambda: show_frame("director_dashboard"),
        'teacher_home': lambda: show_frame("teacher_dashboard"),
        'parent_home': lambda: show_frame("parent_dashboard"),
        'show_frame': show_frame,
        'next': lambda: next_step(),
        'prev': lambda: prev_step(),
        'submit': lambda: submit_form(),
    }
    return nav_commands


def next_step():
    global step_index
    if step_index < 4:
        step_index += 1
        show_frame(f"step{step_index}")

def prev_step():
    global step_index
    if step_index > 1:
        step_index -= 1
        show_frame(f"step{step_index}")

def submit_form():
    # Lógica para enviar el formulario
    messagebox.showinfo("Éxito", "Formulario enviado correctamente")


def initialize_app(root_window):
    global root, frames
    
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
    
    nav_commands = create_nav_commands()
    
    frames["login"] = create_login_screen(main_frame)
    frames["login"].grid(row=0, column=0, sticky="nsew")
    
    frames["step1"] = create_step_screen(main_frame, 1, create_step1)
    frames["step1"].grid(row=0, column=0, sticky="nsew")
    
    frames["step2"] = create_step_screen(main_frame, 2, create_step2)
    frames["step2"].grid(row=0, column=0, sticky="nsew")
    
    frames["step3"] = create_step_screen(main_frame, 3, create_step3)
    frames["step3"].grid(row=0, column=0, sticky="nsew")
    
    frames["step4"] = create_step_screen(main_frame, 4, create_step4)
    frames["step4"].grid(row=0, column=0, sticky="nsew")
    
    frames["dashboard"] = create_admin_dashboard(main_frame, nav_commands)
    frames["dashboard"].grid(row=0, column=0, sticky="nsew")
    
    frames["director_dashboard"] = create_director_dashboard(main_frame, nav_commands)
    frames["director_dashboard"].grid(row=0, column=0, sticky="nsew")
    
    frames["teacher_dashboard"] = create_teacher_dashboard(main_frame, nav_commands)
    frames["teacher_dashboard"].grid(row=0, column=0, sticky="nsew")
    
    frames["assignment_teacher"] = create_assignment_teacher(main_frame, nav_commands)
    frames["assignment_teacher"].grid(row=0, column=0, sticky="nsew")
    
    frames["observer_teacher"] = create_observer_teacher(main_frame, nav_commands)
    frames["observer_teacher"].grid(row=0, column=0, sticky="nsew")
    
    frames["parent_dashboard"] = create_parent_dashboard(main_frame, nav_commands)
    frames["parent_dashboard"].grid(row=0, column=0, sticky="nsew")
    
    frames["consult_parent"] = create_consult_parent(main_frame, nav_commands)
    frames["consult_parent"].grid(row=0, column=0, sticky="nsew")
    
    frames["citation_generator"] = create_citation_generator(main_frame, nav_commands)
    frames["citation_generator"].grid(row=0, column=0, sticky="nsew")
    
    frames["groups_manager"] = create_groups_manager(main_frame, nav_commands)
    frames["groups_manager"].grid(row=0, column=0, sticky="nsew")
    
    frames["achievements_manager"] = create_achievements_manager(main_frame, nav_commands)
    frames["achievements_manager"].grid(row=0, column=0, sticky="nsew")
    
    frames["student_manager"] = create_student_manager(main_frame, nav_commands)
    frames["student_manager"].grid(row=0, column=0, sticky="nsew")
    
    frames["evaluations_manager"] = create_evaluations_manager(main_frame, nav_commands)
    frames["evaluations_manager"].grid(row=0, column=0, sticky="nsew")
    
    frames["assigned_courses"] = create_assigned_courses(main_frame, nav_commands)
    frames["assigned_courses"].grid(row=0, column=0, sticky="nsew")
    
    frames["report_generator"] = create_report_generator(main_frame, nav_commands)
    frames["report_generator"].grid(row=0, column=0, sticky="nsew")
    
    show_frame("login")


if __name__ == "__main__":
    root_window = tk.Tk()
    initialize_app(root_window)
    root_window.mainloop()
