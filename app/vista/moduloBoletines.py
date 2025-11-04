import tkinter as tk
import tkinter.ttk as ttk
from config import *

def create_report_generator(master, nav_commands):
    """Crea la interfaz de generación de boletines."""
    frame = tk.Frame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Frame(frame, bg=COLOR_HEADER_PRE)
    header.grid(row=0, column=0, sticky="ew")
    
    tk.Button(header, text="← Volver", command=lambda: nav_commands['teacher_home'](),
              bg=COLOR_HEADER_PRE, fg=COLOR_TEXT_PRE, font=FONT_P_BOLD,
              bd=0, highlightthickness=0).pack(side="left", padx=20, pady=15)
              
    tk.Label(header, text="Generación de Boletines", bg=COLOR_HEADER_PRE,
             fg=COLOR_TEXT_PRE, font=FONT_H1).pack(side="left", padx=20, pady=15)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    # Filtros superiores
    filter_frame = tk.Frame(content, bg="#ffffff")
    filter_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(filter_frame, text="Grupo:", bg="#ffffff").pack(side="left")
    ttk.Combobox(filter_frame, values=["Párvulos A"]).pack(side="left", padx=5)
    
    tk.Label(filter_frame, text="Periodo:", bg="#ffffff").pack(side="left", padx=(20, 0))
    ttk.Combobox(filter_frame, values=["Periodo 1", "Periodo 2"]).pack(side="left", padx=5)
    
    ttk.Button(filter_frame, text="Generar Todos").pack(side="right")
    
    # Lista de estudiantes
    tree = ttk.Treeview(content, columns=("id", "nombre", "estado", "acciones"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Estudiante")
    tree.heading("estado", text="Estado")
    tree.heading("acciones", text="Acciones")
    
    tree.column("id", width=50)
    tree.column("nombre", width=200)
    tree.column("estado", width=150)
    tree.column("acciones", width=200)
    
    # Datos de ejemplo
    estudiantes = [
        ("001", "Emma Rodríguez", "Pendiente", ""),
        ("002", "Lucas Martínez", "Generado", ""),
        ("003", "Sofía García", "Pendiente", ""),
        ("004", "Diego López", "Generado", ""),
    ]
    
    for est in estudiantes:
        tree.insert("", "end", values=est)
    
    tree.pack(fill="both", expand=True)
    
    # Panel de vista previa
    preview_frame = tk.Frame(content, bg="#ffffff", relief="solid", borderwidth=1)
    preview_frame.pack(fill="x", pady=(20, 0))
    
    tk.Label(preview_frame, text="Vista Previa del Boletín", bg="#ffffff", font=FONT_P_BOLD).pack(anchor="w", padx=20, pady=10)
    
    preview_area = tk.Frame(preview_frame, bg="#ffffff", height=200)
    preview_area.pack(fill="x", padx=20, pady=10)
    preview_area.pack_propagate(False)
    
    tk.Label(preview_area, text="Seleccione un estudiante para ver la vista previa de su boletín", 
             bg="#ffffff", fg=COLOR_TEXT_MUTED).pack(expand=True)
    
    button_frame = tk.Frame(preview_frame, bg="#ffffff")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    ttk.Button(button_frame, text="Generar PDF").pack(side="right", padx=5)
    ttk.Button(button_frame, text="Vista Previa").pack(side="right")
    
    return frame