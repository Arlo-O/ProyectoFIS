import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from ..config import *

# ✅ NUEVO: Importar decorador RBAC
from app.services.rbac_service import require_permission

# ✅ CU-18: Importar servicios y diálogo de admisión
from app.services.servicio_aspirante import ServicioAspirante
from ..components.dialogo_admision import abrir_dialogo_admision


# ✅ PROTEGIDO: Requiere permiso "acceder_estudiante"
@require_permission("acceder_estudiante")
def create_student_manager(master, nav_commands):
    """Crea la interfaz completa de gestión de estudiantes con 3 pestañas."""
    
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
        command=lambda: nav_commands['director_home'](),
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_P_BOLD,
        bd=0,
        highlightthickness=0,
        relief="flat"
    ).pack(side="left", padx=25, pady=20)
    
    tk.Label(
        header,
        text="👨‍🎓 Gestión de Estudiantes",
        bg=COLOR_HEADER_PRE,
        fg=COLOR_TEXT_PRE,
        font=FONT_H1
    ).pack(side="left", padx=30, pady=20)
    
    # Contenido Principal
    content = tk.Frame(frame, bg="#ffffff")
    content.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
    content.grid_columnconfigure(0, weight=1)
    
    # Notebook principal con pestañas
    notebook = ttk.Notebook(content)
    notebook.pack(fill="both", expand=True, pady=(0, 20))
    
    # === PESTAÑA 1: ESTUDIANTES ACTIVOS ===
    tab_active = ttk.Frame(notebook)
    notebook.add(tab_active, text="👥 Estudiantes Activos")
    
    # Filtros y controles
    filter_frame = tk.Frame(tab_active, bg="#f8f9fa", relief="solid", bd=1)
    filter_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    filter_inner = tk.Frame(filter_frame, bg="#f8f9fa", padx=25, pady=20)
    filter_inner.pack()
    
    tk.Label(
        filter_inner,
        text="🎓 Grado:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    grade_combo = ttk.Combobox(
        filter_inner,
        values=["Todos", "Preescolar", "Transición", "Primero", "Segundo"],
        width=15,
        state="readonly"
    )
    grade_combo.set("Todos")
    grade_combo.pack(side="left", padx=(0, 25))
    
    tk.Label(
        filter_inner,
        text="👥 Grupo:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    group_combo = ttk.Combobox(
        filter_inner,
        values=["Todos", "A", "B", "C", "D"],
        width=12,
        state="readonly"
    )
    group_combo.set("Todos")
    group_combo.pack(side="left", padx=(0, 30))
    
    # Botones de acción
    search_var = tk.StringVar()
    tk.Entry(
        filter_inner,
        textvariable=search_var,
        width=20,
        font=FONT_P
    ).pack(side="left", padx=(0, 10))
    
    ttk.Button(
        filter_inner,
        text="🔍 Buscar",
        style="AdminBlue.TButton"
    ).pack(side="left", padx=(0, 10))
    
    ttk.Button(
        filter_inner,
        text="➕ Nuevo Estudiante",
        style="AdminGreen.TButton"
    ).pack(side="right", padx=(10, 5))
    
    ttk.Button(
        filter_inner,
        text="📄 Exportar Lista",
        style="Pre.TButton"
    ).pack(side="right")
    
    # Tabla con scrollbar
    tree_container = tk.Frame(tab_active)
    tree_container.pack(fill="both", expand=True, padx=20)
    
    tree_scroll = ttk.Scrollbar(tree_container)
    tree_scroll.pack(side="right", fill="y")
    
    columns = ("id", "nombre", "grado", "grupo", "asistencia", "estado", "acciones")
    tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        selectmode="browse",
        yscrollcommand=tree_scroll.set,
        height=12
    )
    tree_scroll.config(command=tree.yview)
    tree.pack(side="left", fill="both", expand=True)
    
    # Configurar columnas
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Nombre Completo")
    tree.heading("grado", text="Grado")
    tree.heading("grupo", text="Grupo")
    tree.heading("asistencia", text="Asistencia")
    tree.heading("estado", text="Estado")
    tree.heading("acciones", text="Acciones")
    
    tree.column("id", width=60, anchor="center")
    tree.column("nombre", width=280)
    tree.column("grado", width=100, anchor="center")
    tree.column("grupo", width=80, anchor="center")
    tree.column("asistencia", width=100, anchor="center")
    tree.column("estado", width=100, anchor="center")
    tree.column("acciones", width=150)
    
    # Datos de ejemplo
    estudiantes = [
        ("001", "Emma Rodríguez González", "Preescolar", "A", "98%", "Activo", "Ver/Editar"),
        ("002", "Lucas Martínez Pérez", "Preescolar", "A", "95%", "Activo", "Ver/Editar"),
        ("003", "Sofía García López", "Transición", "B", "92%", "Activo", "Ver/Editar"),
        ("004", "Diego López Ramírez", "Preescolar", "C", "97%", "Activo", "Ver/Editar"),
        ("005", "Valentina Torres", "Primero", "A", "89%", "Activo", "Ver/Editar"),
        ("006", "Mateo Hernández", "Preescolar", "A", "96%", "Suspendido", "Ver/Editar"),
    ]
    
    for est in estudiantes:
        tree.insert("", "end", values=est)
    
    # === PESTAÑA 2: HOJA DE VIDA ===
    tab_record = ttk.Frame(notebook)
    notebook.add(tab_record, text="📋 Hoja de Vida")
    
    record_container = tk.Frame(tab_record, bg="#ffffff")
    record_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Selector de estudiante
    selector_frame = tk.Frame(record_container, bg="#f8f9fa", relief="solid", bd=1)
    selector_frame.pack(fill="x", pady=(0, 25))
    
    selector_inner = tk.Frame(selector_frame, bg="#f8f9fa", padx=25, pady=20)
    selector_inner.pack()
    
    tk.Label(
        selector_inner,
        text="👤 Estudiante:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left")
    
    student_combo = ttk.Combobox(
        selector_inner,
        values=["Emma Rodríguez González - Preescolar A", "Lucas Martínez Pérez - Preescolar A"],
        width=35,
        state="readonly"
    )
    student_combo.set("Emma Rodríguez González - Preescolar A")
    student_combo.pack(side="left", padx=15)
    
    ttk.Button(
        selector_inner,
        text="🔄 Cargar Datos",
        style="AdminBlue.TButton"
    ).pack(side="left", padx=15)
    
    ttk.Button(
        selector_inner,
        text="📄 Generar PDF",
        style="Pre.TButton"
    ).pack(side="right", padx=(0, 10))
    
    ttk.Button(
        selector_inner,
        text="✏️ Editar Registro",
        style="AdminGreen.TButton"
    ).pack(side="right")
    
    # Sub-notebook para detalles
    detail_notebook = ttk.Notebook(record_container)
    detail_notebook.pack(fill="both", expand=True)
    
    # Subpestaña 1: Información Personal
    personal_tab = ttk.Frame(detail_notebook)
    detail_notebook.add(personal_tab, text="Información Personal")
    
    personal_frame = tk.Frame(personal_tab, padx=30, pady=30)
    personal_frame.pack(fill="both", expand=True)
    personal_frame.grid_columnconfigure(1, weight=1)
    
    personal_data = [
        ("Nombre Completo:", "Emma Rodríguez González"),
        ("Fecha Nacimiento:", "15/03/2022"),
        ("Edad:", "3 años"),
        ("Género:", "Femenino"),
        ("Grado:", "Preescolar A"),
        ("Tutor Principal:", "María González"),
        ("Teléfono:", "+57 300 123 4567"),
        ("Email:", "maria.gonzalez@email.com")
    ]
    
    for i, (label, value) in enumerate(personal_data):
        tk.Label(personal_frame, text=label, font=FONT_P_BOLD).grid(row=i, column=0, sticky="e", padx=15, pady=8)
        value_label = tk.Label(personal_frame, text=value, font=FONT_P, fg=COLOR_HEADER_PRE)
        value_label.grid(row=i, column=1, sticky="w", padx=15, pady=8)
    
    # Subpestaña 2: Historial Académico
    academic_tab = ttk.Frame(detail_notebook)
    detail_notebook.add(academic_tab, text="Historial Académico")
    
    # === PESTAÑA 3: ASPIRANTES ===
    tab_applicants = ttk.Frame(notebook)
    notebook.add(tab_applicants, text="📋 Aspirantes (Preinscripciones)")
    
    applicants_container = tk.Frame(tab_applicants, bg="#ffffff")
    applicants_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Filtros aspirantes
    applicants_filter = tk.Frame(applicants_container, bg="#f8f9fa", relief="solid", bd=1)
    applicants_filter.pack(fill="x", pady=(0, 20))
    
    applicants_filter_inner = tk.Frame(applicants_filter, bg="#f8f9fa", padx=25, pady=20)
    applicants_filter_inner.pack()
    
    tk.Label(
        applicants_filter_inner,
        text="📅 Estado:",
        bg="#f8f9fa",
        font=FONT_P_BOLD
    ).pack(side="left", padx=(0, 10))
    
    status_combo = ttk.Combobox(
        applicants_filter_inner,
        values=["Todos", "pendiente", "en_proceso", "admitido", "rechazado"],
        width=15,
        state="readonly"
    )
    status_combo.set("Todos")
    status_combo.pack(side="left", padx=(0, 25))
    
    # CU-18: Botón para diligenciar admisión
    def on_diligenciar_admision():
        """PASO 2 del CU-18: Directivo hace clic en 'Diligenciar admisión'"""
        seleccion = applicants_tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Selección Requerida",
                "Por favor, seleccione un aspirante de la tabla.",
                parent=frame
            )
            return
        
        # Obtener datos del aspirante seleccionado
        item = applicants_tree.item(seleccion[0])
        valores = item['values']
        id_aspirante = valores[0]
        nombre_aspirante = valores[1]
        estado_actual = valores[4]
        
        # Validar que el aspirante esté en estado "en_proceso"
        if estado_actual not in ["en_proceso", "pendiente"]:
            messagebox.showinfo(
                "Estado No Válido",
                f"Solo se pueden admitir/rechazar aspirantes en estado 'en_proceso' o 'pendiente'.\n\n"
                f"Estado actual: {estado_actual}",
                parent=frame
            )
            return
        
        # PASO 3: Abrir diálogo de admisión
        abrir_dialogo_admision(
            frame,
            id_aspirante,
            nombre_aspirante,
            callback_actualizar=lambda: cargar_aspirantes()
        )
    
    ttk.Button(
        applicants_filter_inner,
        text="✅ Diligenciar Admisión",
        style="AdminGreen.TButton",
        command=on_diligenciar_admision
    ).pack(side="right", padx=(10, 5))
    
    ttk.Button(
        applicants_filter_inner,
        text="🔄 Actualizar Lista",
        style="Pre.TButton",
        command=lambda: cargar_aspirantes()
    ).pack(side="right")
    
    # Tabla aspirantes
    applicants_tree_container = tk.Frame(applicants_container)
    applicants_tree_container.pack(fill="both", expand=True)
    
    applicants_scroll = ttk.Scrollbar(applicants_tree_container)
    applicants_scroll.pack(side="right", fill="y")
    
    applicants_columns = ("id", "nombre", "fecha", "grado_deseado", "estado", "telefono")
    applicants_tree = ttk.Treeview(
        applicants_tree_container,
        columns=applicants_columns,
        show="headings",
        yscrollcommand=applicants_scroll.set,
        height=12
    )
    applicants_scroll.config(command=applicants_tree.yview)
    applicants_tree.pack(side="left", fill="both", expand=True)
    
    # Configurar columnas aspirantes
    applicants_tree.heading("id", text="ID")
    applicants_tree.heading("nombre", text="Nombre Aspirante")
    applicants_tree.heading("fecha", text="Fecha Solicitud")
    applicants_tree.heading("grado_deseado", text="Grado Deseado")
    applicants_tree.heading("estado", text="Estado")
    applicants_tree.heading("telefono", text="Teléfono")
    
    applicants_tree.column("id", width=60)
    applicants_tree.column("nombre", width=250)
    applicants_tree.column("fecha", width=120, anchor="center")
    applicants_tree.column("grado_deseado", width=120)
    applicants_tree.column("estado", width=100, anchor="center")
    applicants_tree.column("telefono", width=120)
    
    def cargar_aspirantes(filtro_estado=None):
        """Carga los aspirantes desde la base de datos"""
        # Limpiar tabla
        for item in applicants_tree.get_children():
            applicants_tree.delete(item)
        
        # Obtener aspirantes del servicio
        servicio = ServicioAspirante()
        exito, aspirantes, mensaje = servicio.obtener_listado_aspirantes()
        
        if not exito:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los aspirantes:\n{mensaje}",
                parent=frame
            )
            return
        
        # Filtrar por estado si se especifica
        estado_filtro = status_combo.get()
        if estado_filtro != "Todos":
            aspirantes = [asp for asp in aspirantes if asp.get('estado_proceso') == estado_filtro]
        
        # Insertar en la tabla
        for asp in aspirantes:
            fecha_str = asp['fecha_solicitud'].strftime('%d/%m/%Y') if asp['fecha_solicitud'] else "N/A"
            applicants_tree.insert("", "end", values=(
                asp['id_aspirante'],
                asp['nombre_completo'],
                fecha_str,
                asp['grado_solicitado'] or "N/A",
                asp['estado_proceso'] or "pendiente",
                asp['telefono'] or "N/A"
            ))
        
        # Actualizar contador
        total = len(applicants_tree.get_children())
        # Aquí podrías actualizar un label con el contador si lo deseas
    
    # Cargar aspirantes al inicio
    cargar_aspirantes()
    
    # Vincular cambio de filtro
    status_combo.bind("<<ComboboxSelected>>", lambda e: cargar_aspirantes())
    
    return frame
