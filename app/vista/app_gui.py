import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

from config import *
from gui_styles import configure_styles
from session_manager import set_current_role

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
step = -1
canvases = {}

users = {
    "admin": {"pass": "admin123", "rol": "admin"},
    "director": {"pass": "dir123", "rol": "director"},
    "profe": {"pass": "prof123", "rol": "teacher"},
    "papa": {"pass": "papa123", "rol": "parent"}
}

user_entry_ref = None
pass_entry_ref = None

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
   
    
    if user_entry_ref is None or pass_entry_ref is None:
        messagebox.showerror("Error", "La interfaz no se ha inicializado correctamente.")
        return

    user = user_entry_ref.get().lower()
    password = pass_entry_ref.get()

    if user == user_entry_ref.placeholder.lower() or password == pass_entry_ref.placeholder:
        messagebox.showerror("Error de Login", "Por favor, ingrese usuario y contraseña.")
        return
    
    if user in USER_CREDENTIALS and USER_CREDENTIALS[user]["password"] == password:
        role = USER_CREDENTIALS[user]["role"]
        
     
        set_current_role(role) 
        
        role_map = {
            "admin": "dashboard",
            "director": "director_dashboard",
            "teacher": "teacher_dashboard",
            "parent": "parent_dashboard",
        }
        
        target_frame = role_map.get(role)
        if target_frame:
            show_frame(target_frame)
            
            user_entry_ref.delete(0, tk.END)
            pass_entry_ref.delete(0, tk.END)
            user_entry_ref.insert(0, user_entry_ref.placeholder)
            pass_entry_ref.insert(0, pass_entry_ref.placeholder)
            user_entry_ref.config(fg=COLOR_TEXT_PLACEHOLDER)
            pass_entry_ref.config(fg=COLOR_TEXT_PLACEHOLDER, show="")
            
        else:
            messagebox.showerror("Error de Rol", "Rol de usuario no reconocido.")
            
    else:
        messagebox.showerror("Error de Login", "Credenciales incorrectas.")


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

def create_login_column(parent, login_command):
    global user_entry_ref, pass_entry_ref 
    
    column = tk.Frame(parent, bg=COLOR_BG_LOGIN)
    tk.Label(column, text="Sistema de Gestión Académica", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_H1).pack(fill="x", side="top", ipady=30)
    tk.Label(column, text="Colegio Pequeño - Educación Inicial", bg=COLOR_DARK_BG, fg=COLOR_HEADER_PRE, font=FONT_P).pack(fill="x", side="top", pady=(0, 30))
    
    login_main_container = tk.Frame(column, bg=COLOR_BG_LOGIN)
    login_main_container.pack(expand=True, fill="both")

    login_main = tk.Frame(login_main_container, bg=COLOR_BG_LOGIN, width=350, height=450)
    login_main.place(relx=0.5, rely=0.5, anchor="center") 
    login_main.pack_propagate(False) 
    
    tk.Label(login_main, text="Autenticación de Usuario", bg=COLOR_BG_LOGIN, fg=COLOR_TEXT_DARK, font=FONT_H2).pack(anchor="w", pady=(0, 20))