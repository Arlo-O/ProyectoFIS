import tkinter as tk
import tkinter.ttk as ttk
from .config import *


def create_assigned_courses(master, nav_commands):
    """Panel de cursos asignados para profesores con tarjetas interactivas."""
    
    frame = tk.Frame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Frame(frame, bg=COLOR_HEADER_PRE, height=70)
    header.grid(row=0, column=0, sticky="ew")
    header.pack_propagate(False)
    
    tk.Button(
        header,
        text="← Volver al Dashboard",
        command=lambda: nav_commands['teacher_home'](),
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        relief="flat"
    ).pack(side="left", padx=25, pady=20)
    
    tk.Label(
        header,
        text="📚 Mis Cursos Asignados",
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_H1
    ).pack(side="left", padx=30, pady=20)
    
    # Contenido principal
    content = tk.Frame(frame, bg="#f8f9fa")
    content.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    content.grid_columnconfigure(0, weight=1)
    
    # Título de sección
    title_frame = tk.Frame(content, bg="#f8f9fa")
    title_frame.pack(fill="x", pady=(0, 25))
    
    tk.Label(
        title_frame,
        text="Tus grupos asignados este período:",
        bg="#f8f9fa",
        fg=COLOR_TEXT_DARK,
        font=FONT_H2
    ).pack(side="left")
    
    tk.Label(
        title_frame,
        text="Período: Noviembre - Diciembre 2025",
        bg="#f8f9fa",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD
    ).pack(side="right")
    
    # Scrollable container para cursos
    scroll_container = tk.Frame(content)
    scroll_container.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(scroll_container, bg="#f8f9fa", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Función para crear tarjeta de curso
    def create_course_card(parent, title, students_count, schedule, color=COLOR_HEADER_PRE, actions=True):
        card = tk.Frame(
            parent,
            bg="#ffffff",
            padx=30,
            pady=25,
            relief="solid",
            bd=2,
            highlightbackground=COLOR_TEST_BORDER,
            highlightthickness=2
        )
        card.pack(fill="x", pady=15, padx=20)
        
        # Header del curso con gradiente simulado
        header_frame = tk.Frame(
            card,
            bg=color,
            height=60
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"👨‍🏫 {title}",
            font=FONT_H2,
            bg=color,
            fg=COLOR_TEXT_LIGHT
        ).pack(side="left", padx=25, pady=15)
        
        status_label = tk.Label(
            header_frame,
            text="Activo",
            bg=color,
            fg="#28a745",
            font=FONT_P_BOLD,
            padx=20,
            pady=10,
            relief="solid",
            bd=1
        )
        status_label.pack(side="right", padx=25, pady=15)
        
        # Información del curso
        info_frame = tk.Frame(card, bg="#ffffff")
        info_frame.pack(fill="x", pady=(20, 0))
        
        # Stats en grid
        stats_grid = tk.Frame(info_frame, bg="#ffffff")
        stats_grid.pack(fill="x", pady=(0, 20))
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        
        # Estudiantes
        student_frame = tk.Frame(stats_grid, bg="#e8f5e8", padx=20, pady=15, relief="solid", bd=1)
        student_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        
        tk.Label(
            student_frame,
            text="👥 Estudiantes",
            bg="#e8f5e8",
            fg=COLOR_TEXT_MUTED,
            font=FONT_SMALL
        ).pack(anchor="w")
        tk.Label(
            student_frame,
            text=f"{students_count}",
            bg="#e8f5e8",
            fg="#28a745",
            font=FONT_H2
        ).pack(anchor="w")
        
        # Horario
        schedule_frame = tk.Frame(stats_grid, bg="#e3f2fd", padx=20, pady=15, relief="solid", bd=1)
        schedule_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        tk.Label(
            schedule_frame,
            text="📅 Horario",
            bg="#e3f2fd",
            fg=COLOR_TEXT_MUTED,
            font=FONT_SMALL
        ).pack(anchor="w")
        tk.Label(
            schedule_frame,
            text=schedule,
            bg="#e3f2fd",
            fg=COLOR_HEADER_PRE,
            font=FONT_P_BOLD
        ).pack(anchor="w")
        
        # Botones de acción
        if actions:
            btn_frame = tk.Frame(info_frame, bg="#ffffff")
            btn_frame.pack(fill="x")
            
            ttk.Button(
                btn_frame,
                text="📋 Ver Lista de Estudiantes",
                style="AdminBlue.TButton",
                command=lambda: print(f"Abriendo lista de {title}")
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                btn_frame,
                text="⭐ Ver Logros (CRE)",
                style="Pre.TButton",
                command=lambda: print(f"Abriendo logros de {title}")
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                btn_frame,
                text="📊 Evaluaciones",
                style="AdminGreen.TButton",
                command=lambda: print(f"Abriendo evaluaciones de {title}")
            ).pack(side="left")
    
    # Crear tarjetas de cursos
    create_course_card(
        scrollable_frame,
        "Párvulos A - Grupo Principal",
        "8 estudiantes",
        "Lun-Vie 8:00 AM - 12:00 PM",
        COLOR_HEADER_PRE
    )
    
    create_course_card(
        scrollable_frame,
        "Jardín B - Expresión Artística",
        "12 estudiantes",
        "Mar-Jue 2:00 PM - 4:00 PM",
        "#4a90e2"
    )
    
    create_course_card(
        scrollable_frame,
        "Transición A - Matemáticas Iniciales",
        "10 estudiantes",
        "Lun-Mié-Vie 9:30 AM - 11:00 AM",
        "#f39c12"
    )
    
    create_course_card(
        scrollable_frame,
        "Párvulos C - Lectoescritura",
        "9 estudiantes",
        "Lun-Vie 10:30 AM - 11:30 AM",
        "#27ae60"
    )
    
    # Botón flotante para nuevo curso (placeholder)
    new_course_btn = tk.Button(
        content,
        text="➕ Asignar Nuevo Curso",
        bg=COLOR_ACCENT_ADMIN,
        fg=COLOR_TEXT_LIGHT,
        font=FONT_P_BOLD,
        bd=0,
        relief="flat",
        padx=30,
        pady=12,
        command=lambda: print("Abrir modal nuevo curso")
    )
    new_course_btn.place(relx=0.95, rely=0.95, anchor="se")
    
    return frame
