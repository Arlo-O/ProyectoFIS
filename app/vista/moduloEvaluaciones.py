import tkinter as tk
import tkinter.ttk as ttk
from config import *


def create_evaluations_manager(master, nav_commands):
    """Interfaz de gestión de evaluaciones."""
    
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
        text="📊 Gestión de Evaluaciones",
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_H1
    ).pack(side="left", padx=30, pady=20)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    content.grid_columnconfigure(0, weight=1)
    
    # Filtros superiores
    filter_frame = tk.Frame(content, bg="#f8f9fa", relief="solid", bd=1, padx=25, pady=25)
    filter_frame.pack(fill="x", pady=(0, 25))
    
    # Grupo
    tk.Label(
        filter_frame,
        text="👥 Grupo:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    group_combo = ttk.Combobox(
        filter_frame,
        values=["Párvulos A", "Párvulos B", "Transición A", "Jardín B"],
        width=15,
        state="readonly"
    )
    group_combo.set("Párvulos A")
    group_combo.pack(side="left", padx=(0, 25))
    
    # Periodo
    tk.Label(
        filter_frame,
        text="📅 Período:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    period_combo = ttk.Combobox(
        filter_frame,
        values=["Periodo 1 (Nov-Dic 2025)", "Periodo 2 (Ene-Feb 2026)"],
        width=20,
        state="readonly"
    )
    period_combo.set("Periodo 1 (Nov-Dic 2025)")
    period_combo.pack(side="left", padx=(0, 30))
    
    # Búsqueda
    search_var = tk.StringVar()
    tk.Label(
        filter_frame,
        text="🔍 Buscar:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 5))
    
    tk.Entry(
        filter_frame,
        textvariable=search_var,
        width=20,
        font=FONT_P,
        relief="solid"
    ).pack(side="left", padx=(0, 20))
    
    # Botones principales
    ttk.Button(
        filter_frame,
        text="➕ Nueva Evaluación",
        style="AdminBlue.TButton",
        command=lambda: print("Abrir modal nueva evaluación")
    ).pack(side="right", padx=(10, 5))
    
    ttk.Button(
        filter_frame,
        text="📄 Exportar Reporte",
        style="Pre.TButton"
    ).pack(side="right")
    
    # Lista de evaluaciones con scrollbar
    list_frame = tk.LabelFrame(
        content,
        text="📋 Evaluaciones del Grupo Párvulos A - Período 1",
        bg="#ffffff",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        padx=25,
        pady=20,
        relief="solid",
        bd=2
    )
    list_frame.pack(fill="both", expand=True, pady=(0, 25))
    
    tree_container = tk.Frame(list_frame)
    tree_container.pack(fill="both", expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_container)
    tree_scroll.pack(side="right", fill="y")
    
    columns = ("id", "estudiante", "logro", "evaluacion", "fecha", "acciones")
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
    tree.heading("estudiante", text="Estudiante")
    tree.heading("logro", text="Logro Evaluado")
    tree.heading("evaluacion", text="Evaluación")
    tree.heading("fecha", text="Fecha")
    tree.heading("acciones", text="Acciones")
    
    tree.column("id", width=60, anchor="center")
    tree.column("estudiante", width=180)
    tree.column("logro", width=320)
    tree.column("evaluacion", width=120, anchor="center")
    tree.column("fecha", width=100, anchor="center")
    tree.column("acciones", width=140)
    
    # Datos de ejemplo realistas
    evaluaciones = [
        ("EVL001", "Emma Rodríguez", "Reconocimiento números 1-10", "Excelente", "24/11/2025", "Editar/Eliminar"),
        ("EVL002", "Lucas Martínez", "Concentración 15 min", "Bueno", "21/11/2025", "Editar/Eliminar"),
        ("EVL003", "Sofía García", "Equilibrio motor fino", "Excelente", "17/11/2025", "Editar/Eliminar"),
        ("EVL004", "Diego López", "Compartir juguetes", "Muy Bueno", "14/11/2025", "Editar/Eliminar"),
        ("EVL005", "Valentina Torres", "Colores primarios", "Excelente", "10/11/2025", "Editar/Eliminar"),
        ("EVL006", "Mateo Hernández", "Secuencias simples", "Bueno", "08/11/2025", "Editar/Eliminar"),
    ]
    
    for evl in evaluaciones:
        tree.insert("", "end", values=evl)
    
    # Panel inferior de detalle/edición
    detail_frame = tk.LabelFrame(
        content,
        text="✏️ Detalle y Edición de Evaluación",
        bg="#ffffff",
        fg=COLOR_HEADER_PRE,
        font=FONT_P_BOLD,
        padx=25,
        pady=25,
        relief="solid",
        bd=2
    )
    detail_frame.pack(fill="x")
    
    # Selector de estudiante
    selector_frame = tk.Frame(detail_frame, bg="#ffffff")
    selector_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        selector_frame,
        text="👤 Estudiante:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    student_combo = ttk.Combobox(
        selector_frame,
        values=["Emma Rodríguez", "Lucas Martínez", "Sofía García", "Diego López"],
        width=25,
        state="readonly"
    )
    student_combo.set("Emma Rodríguez")
    student_combo.pack(side="left", padx=(0, 20))
    
    ttk.Button(
        selector_frame,
        text="🔄 Cargar Evaluación",
        style="AdminBlue.TButton"
    ).pack(side="left")
    
    # Formulario principal
    form_frame = tk.Frame(detail_frame, bg="#ffffff")
    form_frame.pack(fill="x")
    form_frame.grid_columnconfigure(1, weight=1)
    
    # Logro
    tk.Label(
        form_frame,
        text="🎯 Logro:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).grid(row=0, column=0, sticky="e", padx=15, pady=10)
    
    logro_combo = ttk.Combobox(
        form_frame,
        values=[
            "Reconocimiento números 1-10",
            "Concentración sostenida",
            "Equilibrio motor fino",
            "Habilidades sociales",
            "Identificación colores"
        ],
        width=40,
        state="readonly"
    )
    logro_combo.set("Reconocimiento números 1-10")
    logro_combo.grid(row=0, column=1, sticky="ew", padx=15, pady=10)
    
    # Evaluación (rating)
    tk.Label(
        form_frame,
        text="⭐ Evaluación:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).grid(row=1, column=0, sticky="e", padx=15, pady=10)
    
    eval_combo = ttk.Combobox(
        form_frame,
        values=["Excelente", "Muy Bueno", "Bueno", "En Desarrollo", "Requiere Apoyo"],
        width=25,
        state="readonly"
    )
    eval_combo.set("Excelente")
    eval_combo.grid(row=1, column=1, sticky="w", padx=15, pady=10)
    
    # Comentarios
    tk.Label(
        form_frame,
        text="💬 Comentarios:",
        bg="#ffffff",
        font=FONT_P_BOLD
    ).grid(row=2, column=0, sticky="ne", padx=15, pady=10)
    
    comments_text = tk.Text(
        form_frame,
        height=4,
        width=50,
        font=FONT_P,
        relief="solid",
        wrap="word"
    )
    comments_text.grid(row=2, column=1, sticky="ew", padx=15, pady=10)
    
    btn_frame = tk.Frame(detail_frame, bg="#ffffff")
    btn_frame.pack(fill="x", pady=20)
    
    ttk.Button(
        btn_frame,
        text="💾 Guardar Evaluación",
        style="AdminBlue.TButton"
    ).pack(side="right", padx=(0, 10))
    
    ttk.Button(
        btn_frame,
        text="❌ Cancelar",
        style="AdminGreen.TButton"
    ).pack(side="right", padx=(0, 10))
    
    ttk.Button(
        btn_frame,
        text="📤 Enviar a Acudientes",
        style="Pre.TButton"
    ).pack(side="right")
    
    # Evento de selección en tabla
    def on_tree_select(event):
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            values = item['values']
            student_combo.set(values[1])
            logro_combo.set(values[2])
            eval_combo.set(values[3])
            comments_text.delete("1.0", tk.END)
            comments_text.insert("1.0", f"Evaluación automática: {values[2]} - {values[3]}")
    
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    
    return frame
