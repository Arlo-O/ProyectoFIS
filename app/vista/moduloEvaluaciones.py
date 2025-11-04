import tkinter as tk
import tkinter.ttk as ttk
from config import *

def create_evaluations_manager(master, nav_commands):
    """Crea la interfaz de gestión de evaluaciones."""
    frame = tk.Frame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Frame(frame, bg=COLOR_HEADER_PRE)
    header.grid(row=0, column=0, sticky="ew")
    
    tk.Button(header, text="← Volver", command=lambda: nav_commands['teacher_home'](),
              bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_P_BOLD,
              bd=0, highlightthickness=0).pack(side="left", padx=20, pady=15)
              
    tk.Label(header, text="Gestión de Evaluaciones", bg=COLOR_HEADER_PRE,
             fg=COLOR_TEXT_PRE, font=FONT_H1).pack(side="left", padx=20, pady=15)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    # Filtros superiores
    filter_frame = tk.Frame(content, bg="#ffffff")
    filter_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(filter_frame, text="Grupo:", bg="#ffffff").pack(side="left")
    ttk.Combobox(filter_frame, values=["Grupo 1", "Grupo 2"]).pack(side="left", padx=5)
    
    tk.Label(filter_frame, text="Periodo:", bg="#ffffff").pack(side="left", padx=(20, 0))
    ttk.Combobox(filter_frame, values=["Periodo 1", "Periodo 2"]).pack(side="left", padx=5)
    
    ttk.Button(filter_frame, text="Nueva Evaluación").pack(side="right")
    
    # Lista de estudiantes y evaluaciones
    tree = ttk.Treeview(content, columns=("id", "estudiante", "logro", "evaluacion", "fecha"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("estudiante", text="Estudiante")
    tree.heading("logro", text="Logro")
    tree.heading("evaluacion", text="Evaluación")
    tree.heading("fecha", text="Fecha")
    
    tree.column("id", width=50)
    tree.column("estudiante", width=200)
    tree.column("logro", width=300)
    tree.column("evaluacion", width=150)
    tree.column("fecha", width=100)
    
    tree.pack(fill="both", expand=True)
    
    # Panel inferior de detalle/edición
    detail_frame = tk.Frame(content, bg="#ffffff", relief="solid", borderwidth=1)
    detail_frame.pack(fill="x", pady=(20, 0))
    
    tk.Label(detail_frame, text="Detalle de Evaluación", bg="#ffffff", font=FONT_P_BOLD).pack(anchor="w", padx=20, pady=10)
    
    form_frame = tk.Frame(detail_frame, bg="#ffffff", padx=20, pady=10)
    form_frame.pack(fill="x")
    
    # Campos del formulario
    tk.Label(form_frame, text="Estudiante:", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(form_frame, state="readonly").grid(row=0, column=1, sticky="w")
    
    tk.Label(form_frame, text="Logro:", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Combobox(form_frame).grid(row=1, column=1, sticky="w")
    
    tk.Label(form_frame, text="Evaluación:", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    text_eval = tk.Text(form_frame, height=4, width=40)
    text_eval.grid(row=2, column=1, sticky="w", pady=5)
    
    button_frame = tk.Frame(detail_frame, bg="#ffffff")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    ttk.Button(button_frame, text="Guardar Evaluación").pack(side="right", padx=5)
    ttk.Button(button_frame, text="Cancelar").pack(side="right")
    
    return frame