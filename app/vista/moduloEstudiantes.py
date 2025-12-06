"""
Archivo: moduloEstudiantes.py
Gestión de Estudiantes del Colegio.

Módulo funcional para directivos que gestiona toda la información de estudiantes.

Funcionalidades:
- Visualización y búsqueda de estudiantes activos
- Gestión de hojas de vida académicas
- Historial académico completo
- Registro de observaciones
- Seguimiento de logros por estudiante
- Gestión de aspirantes (preinscripciones)
- Exportación de listados

Acceso: Directivo (director)
"""

import tkinter as tk
import tkinter.ttk as ttk
from config import *

def create_student_manager(master, nav_commands):
    """Crea la interfaz de gestión de estudiantes."""
    frame = tk.Frame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Frame(frame, bg=COLOR_HEADER_PRE)
    header.grid(row=0, column=0, sticky="ew")
    
    tk.Button(header, text="← Volver", command=lambda: nav_commands['director_home'](),
              bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_P_BOLD,
              bd=0, highlightthickness=0).pack(side="left", padx=20, pady=15)
              
    tk.Label(header, text="Gestión de Estudiantes", bg=COLOR_HEADER_PRE,
             fg=COLOR_TEXT_PRE, font=FONT_H1).pack(side="left", padx=20, pady=15)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    # Pestañas
    notebook = ttk.Notebook(content)
    notebook.pack(fill="both", expand=True)
    
    # Tab: Estudiantes Activos
    tab_active = ttk.Frame(notebook)
    notebook.add(tab_active, text="Estudiantes Activos")
    
    filter_frame = tk.Frame(tab_active)
    filter_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(filter_frame, text="Grado:").pack(side="left")
    ttk.Combobox(filter_frame, values=["Todos", "Preescolar", "Primero", "Segundo"]).pack(side="left", padx=5)
    
    tk.Label(filter_frame, text="Grupo:").pack(side="left", padx=(20, 0))
    ttk.Combobox(filter_frame, values=["Todos", "A", "B", "C"]).pack(side="left", padx=5)
    
    ttk.Button(filter_frame, text="Nuevo Estudiante").pack(side="right")
    ttk.Button(filter_frame, text="Exportar Lista").pack(side="right", padx=5)
    
    # Lista de estudiantes
    tree = ttk.Treeview(tab_active, columns=("id", "nombre", "grado", "grupo", "estado"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Nombre Completo")
    tree.heading("grado", text="Grado")
    tree.heading("grupo", text="Grupo")
    tree.heading("estado", text="Estado")
    
    tree.column("id", width=50)
    tree.column("nombre", width=300)
    tree.column("grado", width=100)
    tree.column("grupo", width=100)
    tree.column("estado", width=100)
    
    tree.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Tab: Hoja de Vida
    tab_record = ttk.Frame(notebook)
    notebook.add(tab_record, text="Hoja de Vida")
    
    record_frame = tk.Frame(tab_record, bg="#ffffff")
    record_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Selector de estudiante
    selector_frame = tk.Frame(record_frame, bg="#ffffff")
    selector_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(selector_frame, text="Estudiante:", bg="#ffffff").pack(side="left")
    ttk.Combobox(selector_frame).pack(side="left", padx=5)
    
    ttk.Button(selector_frame, text="Ver Hoja de Vida").pack(side="right")
    ttk.Button(selector_frame, text="Generar PDF").pack(side="right", padx=5)
    
    # Información detallada
    detail_notebook = ttk.Notebook(record_frame)
    detail_notebook.pack(fill="both", expand=True)
    
    # Subpestañas de la hoja de vida
    tabs_info = [
        ("Información Personal", ["Nombre completo", "Fecha de nacimiento", "Dirección", "Teléfono"]),
        ("Historial Académico", ["Grado actual", "Grados anteriores", "Promedio general"]),
        ("Observaciones", ["Fecha", "Descripción", "Docente"]),
        ("Logros", ["Periodo", "Descripción", "Evaluación"]),
    ]
    
    for tab_name, fields in tabs_info:
        tab = ttk.Frame(detail_notebook)
        detail_notebook.add(tab, text=tab_name)
        
        for i, field in enumerate(fields):
            tk.Label(tab, text=f"{field}:").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            if field == "Descripción":
                tk.Text(tab, height=4, width=40).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            else:
                ttk.Entry(tab, width=40).grid(row=i, column=1, padx=5, pady=5, sticky="w")
    
    # Tab: Aspirantes
    tab_applicants = ttk.Frame(notebook)
    notebook.add(tab_applicants, text="Aspirantes")
    
    applicants_frame = tk.Frame(tab_applicants)
    applicants_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Lista de aspirantes
    applicants_tree = ttk.Treeview(applicants_frame, 
                                  columns=("id", "nombre", "fecha", "grado", "estado"),
                                  show="headings")
    applicants_tree.heading("id", text="ID")
    applicants_tree.heading("nombre", text="Nombre")
    applicants_tree.heading("fecha", text="Fecha Solicitud")
    applicants_tree.heading("grado", text="Grado")
    applicants_tree.heading("estado", text="Estado")
    
    applicants_tree.column("id", width=50)
    applicants_tree.column("nombre", width=300)
    applicants_tree.column("fecha", width=100)
    applicants_tree.column("grado", width=100)
    applicants_tree.column("estado", width=100)
    
    applicants_tree.pack(fill="both", expand=True)
    
    return frame