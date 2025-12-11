# Archivo: app_gui.py

import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import sys
import os
from config import *
from gui_styles import configure_styles 
from session_manager import set_current_role 
from pathlib import Path

# Añadir la ruta del módulo app para importar controladores
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import SessionLocal
from controladores.controlador_login import ControladorLogin

# ======================================================================
# --- IMPORTACIÓN DE MÓDULOS DE INTERFAZ (Se asumen existentes) ---
# ======================================================================
# Nota: Debes asegurar que estos archivos existan y contengan las funciones.
from formGui import create_complete_form
from moduloAdmin import create_admin_dashboard
from moduloDirectivo import create_director_dashboard
from moduloProfesor import create_teacher_dashboard, create_assignment_teacher, create_observer_teacher
from moduloAcudiente import create_parent_dashboard
from moduloCitacion import create_citation_generator
from moduloGrupos import create_groups_manager
from moduloLogros import create_achievements_manager
from moduloEstudiantes import create_student_manager
from moduloEvaluaciones import create_evaluations_manager
from moduloCursosAsignados import create_assigned_courses
from moduloBoletines import create_report_generator


# --- Variables Globales de Estado ---
root = None
frames = {}
step_index = -1
step_canvases = {} 

# --- Credenciales Predeterminadas ---
USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin"},
    "directivo": {"password": "dir123", "role": "director"},
    "profesor": {"password": "prof123", "role": "teacher"},
    "acudiente": {"password": "acu123", "role": "parent"},
}

# --- Referencias a los campos de entrada de Login ---
user_entry_ref = None
pass_entry_ref = None

# ======================================================================
# --- Funciones de Utilidad ---
# ======================================================================

def setup_placeholder(entry, placeholder, is_password=False):
    """Configura el comportamiento de placeholder para un widget Entry."""
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
    """Muestra un frame y actualiza el índice global. Asegura scroll al inicio."""
    global step_index
    frame = frames.get(name)
    if frame:
        for other_frame in frames.values():
            other_frame.grid_remove()
        frame.grid(row=0, column=0, sticky="nsew") # Asegura que se muestre correctamente
        
        if name == "login":
            step_index = -1
        elif name == "preinscription_form":
            # Scroll al inicio del formulario
            if name in step_canvases:
                canvas = step_canvases[name]['canvas']
                root.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(0)

def start_preinscription():
    """Inicia el formulario único completo."""
    show_frame("preinscription_form")

def next_step():
    """Ya no es necesario en el nuevo diseño de formulario único con scroll."""
    pass

def prev_step():
    """Ya no es necesario en el nuevo diseño de formulario único con scroll."""
    pass

# ======================================================================
# --- LÓGICA DE LOGIN (INTEGRADA CON CONTROLADOR) ---
# ======================================================================

def login_to_dashboard():
    """Verifica credenciales usando el controlador, establece el rol y navega."""
    global user_entry_ref, pass_entry_ref
    
    if user_entry_ref is None or pass_entry_ref is None:
        messagebox.showerror("Error", "La interfaz no se ha inicializado correctamente.")
        return

    username = user_entry_ref.get().strip()
    password = pass_entry_ref.get().strip()

    if not username or not password:
        messagebox.showerror("Error de Login", "Por favor, ingrese usuario y contraseña.")
        return
    
    if username == user_entry_ref.placeholder or password == pass_entry_ref.placeholder:
        messagebox.showerror("Error de Login", "Por favor, ingrese usuario y contraseña.")
        return
    
    try:
        # Crear sesión y controlador
        db = SessionLocal()
        controlador = ControladorLogin(db)
        
        # Autenticar usuario
        resultado = controlador.autenticar_usuario(username, password)
        
        if resultado['exitoso']:
            # Obtener el nombre del rol
            rol_nombre = resultado['rol'].nombreRol if resultado['rol'] else 'teacher'
            
            # Establecer rol en sesión
            set_current_role(rol_nombre)
            
            # Mapeo de roles a frames
            role_map = {
                'admin': 'dashboard',
                'administrator': 'dashboard',
                'directivo': 'director_dashboard',
                'director': 'director_dashboard',
                'profesor': 'teacher_dashboard',
                'teacher': 'teacher_dashboard',
                'acudiente': 'parent_dashboard',
                'parent': 'parent_dashboard',
                'observador': 'teacher_dashboard',
                'observer': 'teacher_dashboard',
            }
            
            target_frame = role_map.get(rol_nombre.lower(), 'teacher_dashboard')
            
            messagebox.showinfo("Login Exitoso", resultado['mensaje'])
            show_frame(target_frame)
            
            # Limpiar campos
            user_entry_ref.delete(0, tk.END)
            pass_entry_ref.delete(0, tk.END)
            user_entry_ref.insert(0, user_entry_ref.placeholder)
            pass_entry_ref.insert(0, pass_entry_ref.placeholder)
            user_entry_ref.config(fg=COLOR_TEXT_PLACEHOLDER)
            pass_entry_ref.config(fg=COLOR_TEXT_PLACEHOLDER, show="")
        else:
            messagebox.showerror("Error de Login", resultado['mensaje'])
        
        db.close()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error en el sistema de autenticación: {str(e)}")
        print(f"Error detallado: {e}")



# ======================================================================
# --- Funciones de Creación de Vistas (Login/Preinscripción) ---
# ======================================================================

def create_login_screen(parent_frame):
    """Crea la pantalla de Login/Preinscripción."""
    login_layout = tk.Frame(parent_frame)
    login_layout.grid_columnconfigure(0, weight=1)
    login_layout.grid_columnconfigure(1, weight=1)
    login_layout.grid_rowconfigure(0, weight=1)
    
    login_column = create_login_column(login_layout, login_to_dashboard) 
    login_column.grid(row=0, column=0, sticky="nsew")
    
    pre_column = create_pre_column(login_layout)
    pre_column.grid(row=0, column=1, sticky="nsew")

    return login_layout

def create_login_column(parent, login_command):
    """Columna de autenticación."""
    global user_entry_ref, pass_entry_ref 
    
    column = tk.Frame(parent, bg=COLOR_BG_LOGIN)
    tk.Label(column, text="Sistema de Gestión Académica", bg=COLOR_DARK_BG, fg=COLOR_TEXT_LIGHT, font=FONT_H1).pack(fill="x", side="top", ipady=30)
    tk.Label(column, text="Colegio Pequeño - Educación Inicial", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
    
    login_main_container = tk.Frame(column, bg=COLOR_BG_LOGIN)
    login_main_container.pack(expand=True, fill="both")

    login_main = tk.Frame(login_main_container, bg=COLOR_BG_LOGIN, width=350, height=450)
    login_main.place(relx=0.5, rely=0.5, anchor="center") 
    login_main.pack_propagate(False) 
    
    # --- INFO DE USUARIOS PARA PRUEBA ---
    # info_frame = tk.Frame(login_main, bg="#f0f0f0", padx=10, pady=5)
    # info_frame.pack(fill="x", pady=(0, 20))
    # info_text = "Usuarios para prueba:\n"
    # for user, data in USER_CREDENTIALS.items():
    #     info_text += f"• {user}: {data['password']} ({data['role'].capitalize()})\n"
    
    # tk.Label(info_frame, text=info_text, bg="#f0f0f0", fg=COLOR_TEXT_DARK, font=FONT_P, justify="left", anchor="w").pack(fill="x")
    
    tk.Label(login_main, text="Autenticación de Usuario", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_H2).pack(anchor="w", pady=(0, 20))
    
    tk.Label(login_main, text="Usuario:", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_P_BOLD).pack(anchor="w", pady=(5, 5))
    user_entry_ref = tk.Entry(login_main, font=FONT_P, bg="#f9f9f9", relief="solid", borderwidth=1, width=40)
    user_entry_ref.pack(ipady=8, fill=tk.X)
    setup_placeholder(user_entry_ref, "Ingrese su usuario")
    
    tk.Label(login_main, text="Contraseña:", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_P_BOLD).pack(anchor="w", pady=(15, 5))
    pass_entry_ref = tk.Entry(login_main, font=FONT_P, bg="#f9f9f9", relief="solid", borderwidth=1, width=40)
    pass_entry_ref.pack(ipady=8, fill=tk.X)
    setup_placeholder(pass_entry_ref, "Ingrese su contraseña", is_password=True)
    
    ttk.Button(login_main, text="→ Ingresar al Sistema", style="Login.TButton", command=login_command).pack(fill=tk.X, pady=25) 
    
    tk.Label(login_main, text="El sistema detectará automáticamente su rol según sus credenciales", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_MUTED, font=FONT_SMALL).pack()
    return column

def create_pre_column(parent):
    """Columna de Preinscripción."""
    column = tk.Frame(parent, bg=COLOR_BG_PRE)
    tk.Label(column, text="Preinscripción", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_H1).pack(fill="x", side="top", ipady=30)
    tk.Label(column, text="¿Nuevo en el Colegio? Regístrate aquí", bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD).pack(fill="x", side="top", pady=(0, 30))
    
    pre_main_container = tk.Frame(column, bg=COLOR_BG_PRE)
    pre_main_container.pack(expand=True, fill="both")
    
    process_box = tk.Frame(pre_main_container, bg=COLOR_BG_LOGIN, padx=30, pady=30)
    process_box.config(highlightbackground=COLOR_TEST_BORDER, highlightthickness=1)
    process_box.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(process_box, text="Proceso de Preinscripción", bg=COLOR_BG_LOGIN, fg=COLOR_HEADER_PRE, font=FONT_H2).pack(pady=(0, 20))
    
    def add_step(num, text):
        step_frame = tk.Frame(process_box, bg=COLOR_BG_LOGIN)
        step_frame.pack(fill="x", pady=5)
        tk.Label(step_frame, text=str(num), bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_LIGHT, font=FONT_P_BOLD, width=2, height=1).pack(side="left", padx=(0, 10))
        tk.Label(step_frame, text=text, bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_P).pack(side="left", anchor="w")

    add_step(1, "Completar formulario en línea")
    add_step(2, "Recibir confirmación inmediata")
    add_step(3, "Agendar cita para documentación")
    add_step(4, "Conocer nuestras instalaciones")

    ttk.Button(process_box, text="→ Iniciar Preinscripción", 
               style="Pre.TButton", width=30,
               command=start_preinscription).pack(pady=30)
    return column
    
# ======================================================================
# --- Inicializador Principal ---
# ======================================================================

def initialize_app():
    """Función de inicio que configura el entorno global y registra las vistas."""
    global root, frames, step_canvases
    
    root = tk.Tk()
    root.title("Sistema de Gestión Académica")
    root.geometry("900x700")
    root.resizable(False, False)
    
    configure_styles(root)
    
    root_content_frame = tk.Frame(root, bg=COLOR_BG_LOGIN)
    root_content_frame.pack(fill="both", expand=True)
    root_content_frame.grid_rowconfigure(0, weight=1)
    root_content_frame.grid_columnconfigure(0, weight=1)
    
    # 1. Creación de Login
    frames["login"] = create_login_screen(root_content_frame)

    # Inyección de comandos de navegación
    nav_commands = {
        'next': next_step,
        'prev': prev_step,
        'home': lambda: show_frame("login"), 
        'dashboard_home': lambda: show_frame("dashboard"), 
        'director_home': lambda: show_frame("director_dashboard"), 
        'teacher_home': lambda: show_frame("teacher_dashboard"), 
        'parent_home': lambda: show_frame("parent_dashboard"), 
        'show_frame': show_frame  
    }

    # 2. Frame de Preinscripción (Formulario Único)
    try:
        form_frame, canvas = create_complete_form(root_content_frame, nav_commands)
        frames["preinscription_form"] = form_frame
        step_canvases["preinscription_form"] = {'canvas': canvas}
    except Exception as e:
        print(f"Error creando formulario de preinscripción: {e}")
        # En un entorno real, manejarías la excepción.
        
    # 3. Frames de Dashboard y Módulos por Rol
    frames["dashboard"] = create_admin_dashboard(root_content_frame, nav_commands)
    frames["director_dashboard"] = create_director_dashboard(root_content_frame, nav_commands)
    frames["teacher_dashboard"] = create_teacher_dashboard(root_content_frame, nav_commands)
    frames["parent_dashboard"] = create_parent_dashboard(root_content_frame, nav_commands)
    
    # Módulos compartidos
    frames["groups_manager"] = create_groups_manager(root_content_frame, nav_commands)
    frames["citation_generator"] = create_citation_generator(root_content_frame, nav_commands)
    frames["achievements_manager"] = create_achievements_manager(root_content_frame, nav_commands)
    
    # Módulos específicos del profesor
    frames["assigned_courses"] = create_assigned_courses(root_content_frame, nav_commands)
    frames["evaluations_manager"] = create_evaluations_manager(root_content_frame, nav_commands)
    frames["generate_reports"] = create_report_generator(root_content_frame, nav_commands)
    frames["student_observer"] = create_observer_teacher(root_content_frame, nav_commands)
    frames["assignment_teacher"] = create_assignment_teacher(root_content_frame, nav_commands)
    
    # Módulos específicos del directivo
    frames["student_manager"] = create_student_manager(root_content_frame, nav_commands)
    
    # Asegura que todos los frames estén registrados en la cuadrícula pero ocultos
    for frame in frames.values():
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_remove() 

    # Iniciar la aplicación en la pantalla de Login
    show_frame("login")
    
    root.mainloop()

if __name__ == '__main__':
    initialize_app()