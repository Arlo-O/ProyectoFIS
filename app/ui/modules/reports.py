import tkinter as tk
import tkinter.ttk as ttk
from ..config import *


def create_report_generator(master, nav_commands):
    """Generador de boletines para profesores - Módulo completo."""
    
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
        text="📊 Generación de Boletines",
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_H1
    ).pack(side="left", padx=30, pady=20)
    
    # Contenido principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    content.grid_columnconfigure(0, weight=1)
    
    # Filtros
    filter_frame = tk.Frame(content, bg="#f8f9fa", relief="solid", bd=1)
    filter_frame.pack(fill="x", pady=(0, 25))
    
    filter_inner = tk.Frame(filter_frame, bg="#f8f9fa", padx=25, pady=20)
    filter_inner.pack(fill="x")
    
    # Grupo
    tk.Label(
        filter_inner,
        text="👥 Grupo:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 8))
    
    group_combo = ttk.Combobox(
        filter_inner,
        values=["Párvulos A", "Párvulos B", "Transición A", "Transición B"],
        width=15,
        state="readonly"
    )
    group_combo.set("Párvulos A")
    group_combo.pack(side="left", padx=(0, 25))
    
    # Periodo
    tk.Label(
        filter_inner,
        text="📅 Período:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 8))
    
    period_combo = ttk.Combobox(
        filter_inner,
        values=["Periodo 1 (Nov-Dic 2025)", "Periodo 2 (Ene-Feb 2026)"],
        width=20,
        state="readonly"
    )
    period_combo.set("Periodo 1 (Nov-Dic 2025)")
    period_combo.pack(side="left", padx=(0, 25))
    
    # Botón generar
    ttk.Button(
        filter_inner,
        text="🔄 Generar Lista",
        style="AdminBlue.TButton",
        command=lambda: print("Generando lista de boletines...")
    ).pack(side="right")
    
    # Lista de estudiantes con scrollbar
    list_frame = tk.LabelFrame(
        content,
        text="📋 Estudiantes del Grupo",
        bg="#ffffff",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        padx=20,
        pady=15,
        relief="solid",
        bd=1
    )
    list_frame.pack(fill="both", expand=True, pady=(0, 25))
    
    tree_container = tk.Frame(list_frame)
    tree_container.pack(fill="both", expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_container)
    tree_scroll.pack(side="right", fill="y")
    
    columns = ("id", "nombre", "asistencia", "estado", "acciones")
    tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        selectmode="browse",
        yscrollcommand=tree_scroll.set,
        height=10
    )
    tree_scroll.config(command=tree.yview)
    tree.pack(side="left", fill="both", expand=True)
    
    # Configurar columnas
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Estudiante")
    tree.heading("asistencia", text="Asistencia")
    tree.heading("estado", text="Estado Boletín")
    tree.heading("acciones", text="Acciones")
    
    tree.column("id", width=60, anchor="center")
    tree.column("nombre", width=220)
    tree.column("asistencia", width=100, anchor="center")
    tree.column("estado", width=130, anchor="center")
    tree.column("acciones", width=180)
    
    preview_frame = tk.LabelFrame(
        content,
        text="👁️ Vista Previa del Boletín",
        bg="#ffffff",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        padx=20,
        pady=20,
        relief="solid",
        bd=1
    )
    preview_frame.pack(fill="x")
    
    preview_label = tk.Label(
        preview_frame,
        text="Seleccione un estudiante de la lista para ver la vista previa de su boletín",
        bg="#ffffff",
        fg=COLOR_TEXT_MUTED,
        font=FONT_P,
        pady=30
    )
    preview_label.pack(expand=True)
    
    # Botones de acción preview
    preview_btn_frame = tk.Frame(preview_frame, bg="#ffffff")
    preview_btn_frame.pack(fill="x", pady=(0, 10))
    
    ttk.Button(
        preview_btn_frame,
        text="📄 Generar PDF Individual",
        style="Pre.TButton"
    ).pack(side="right", padx=(0, 10))
    
    ttk.Button(
        preview_btn_frame,
        text="👁️ Vista Previa Completa",
        style="AdminBlue.TButton"
    ).pack(side="right")
    
    # Evento selección estudiante
    def on_tree_select(event):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            student_name = item['values'][1]
            preview_label.config(
                text=f"Vista previa del boletín de:\n{student_name}\n\n📈 Asistencia: {item['values'][2]}\n📊 Estado: {item['values'][3]}\n\n[Simulación de contenido del boletín]"
            )
    
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    
    # Estilo alternado para filas
    def alternate_row_colors(event):
        for i, item_id in enumerate(tree.get_children()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.set(item_id, "id", tree.item(item_id, "values")[0])
            tree.item(item_id, tags=(tag,))
    
    tree.tag_configure("evenrow", background="#f8f9fa")
    tree.tag_configure("oddrow", background="white")
    tree.bind("<Configure>", alternate_row_colors)
    
    return frame
