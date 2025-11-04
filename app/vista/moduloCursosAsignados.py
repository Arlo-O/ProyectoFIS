import tkinter as tk
import tkinter.ttk as ttk
from config import *

def create_assigned_courses(master, nav_commands):
    """Crea la interfaz de cursos asignados al profesor."""
    frame = tk.Frame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Frame(frame, bg=COLOR_HEADER_PRE)
    header.grid(row=0, column=0, sticky="ew")
    
    tk.Button(header, text="← Volver", command=lambda: nav_commands['teacher_home'](),
              bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_P_BOLD,
              bd=0, highlightthickness=0).pack(side="left", padx=20, pady=15)
              
    tk.Label(header, text="Mis Cursos Asignados", bg=COLOR_HEADER_PRE,
             fg=COLOR_TEXT_PRE, font=FONT_H1).pack(side="left", padx=20, pady=15)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    # Lista de cursos
    courses_frame = tk.Frame(content, bg="#ffffff")
    courses_frame.pack(fill="both", expand=True)
    
    # Card para cada curso
    def create_course_card(title, students, schedule):
        card = tk.Frame(courses_frame, bg="#ffffff", relief="solid", bd=1)
        card.pack(fill="x", pady=10, padx=20)
        
        header = tk.Frame(card, bg=COLOR_HEADER_PRE)
        header.pack(fill="x")
        tk.Label(header, text=title, font=FONT_H3, bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE).pack(padx=20, pady=10)
        
        info = tk.Frame(card, bg="#ffffff", padx=20, pady=15)
        info.pack(fill="x")
        
        tk.Label(info, text=f"Estudiantes: {students}", font=FONT_P, bg="#ffffff").pack(anchor="w")
        tk.Label(info, text=f"Horario: {schedule}", font=FONT_P, bg="#ffffff").pack(anchor="w", pady=(5,0))
        
        buttons = tk.Frame(info, bg="#ffffff")
        buttons.pack(fill="x", pady=(15,0))
        
        ttk.Button(buttons, text="Ver Lista").pack(side="left", padx=5)
        ttk.Button(buttons, text="Ver Logros").pack(side="left", padx=5)
        ttk.Button(buttons, text="Evaluaciones").pack(side="left", padx=5)
    
    create_course_card("Párvulos A - Grupo Principal", "8 estudiantes", "Lunes a Viernes 8:00 AM - 12:00 PM")
    create_course_card("Jardín B - Expresión Artística", "12 estudiantes", "Martes y Jueves 2:00 PM - 4:00 PM")
    
    return frame